# Frontend Coding Rules (Next.js / React)

> This file contains coding rules that Coding Agent and QA Agent must follow when working on web-fullstack project frontends.

---

## 1. Project Structure

```
fe-project/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── layout.tsx              # Root layout (fonts, global providers)
│   │   ├── page.tsx
│   │   ├── loading.tsx             # Root Suspense fallback
│   │   ├── not-found.tsx           # 404 page
│   │   ├── error.tsx               # Root error boundary (Client Component)
│   │   ├── global-error.tsx        # Crash-level error boundary
│   │   ├── providers.tsx           # Global Client Provider collection ('use client')
│   │   └── (routes)/               # Route groups — domain-specific folders
│   │       └── {domain}/
│   │           ├── page.tsx
│   │           ├── loading.tsx
│   │           ├── error.tsx
│   │           └── _components/    # Route-local components (not shareable)
│   ├── components/
│   │   ├── ui/                     # Reusable atomic components (Button, Input, etc.)
│   │   └── features/               # Domain-specific composite components
│   ├── hooks/                      # Custom hooks
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts           # Base fetch wrapper
│   │   │   └── {domain}.ts         # Domain-specific API functions
│   │   └── utils/                  # Pure utility functions
│   ├── stores/                     # Zustand stores (client-side global state only)
│   ├── types/
│   │   └── api/                    # API response types (mirror BE schemas)
│   ├── constants/                  # App-wide constants and Enums
│   ├── styles/                     # Global styles
│   └── middleware.ts               # Edge middleware (auth, redirect, etc.)
├── public/
├── tests/
│   ├── components/
│   └── hooks/
├── next.config.ts
├── tsconfig.json
└── .env.example                    # List required env var keys only (no values)
```

---

## 2. TanStack Query Setup

### 2-1. QueryClient Provider (Required Initial Setup)

`layout.tsx` is a Server Component, so you cannot put `QueryClientProvider` directly.
Must create separate `providers.tsx` for separation.

```tsx
// src/app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function AppProviders({ children }: { children: React.ReactNode }) {
  // Wrap with useState to create instance only once per component
  // Direct new QueryClient() creates new instance every render
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 1000 * 60,       // Global default staleTime: 1 minute
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

```tsx
// src/app/layout.tsx — Keep as Server Component
import { AppProviders } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

### 2-2. Data Fetching Strategy Selection Criteria

This decision has the biggest impact on performance and accuracy. Choose pattern based on data characteristics.

| Data Type | Pattern | Location |
|-----------|---------|----------|
| Rarely changes, SEO important | `fetch` + `cache: 'force-cache'` (SSG) | Server Component |
| Periodically changes (minutes~hours) | `fetch` + `next: { revalidate: N }` (ISR) | Server Component |
| Changes every request, auth-dependent | `fetch` + `cache: 'no-store'` (SSR) | Server Component |
| Real-time, user-triggered, post-navigation updates | TanStack Query | Client Component |

### 2-3. Server Component Data Fetching

```typescript
// app/(routes)/products/page.tsx
// ✅ Fetch directly at component level — no prop drilling needed
export default async function ProductsPage() {
  const products = await getProducts();
  return <ProductList products={products} />;
}

// src/lib/api/products.ts
export async function getProducts(): Promise<Product[]> {
  const res = await fetch(`${process.env.API_URL}/products`, {
    next: { revalidate: 60 },           // ISR: revalidate every 60 seconds
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) throw new Error('Failed to fetch products');
  const data: ApiResponse<Product[]> = await res.json();
  return data.data ?? [];
}
```

### 2-4. Prefetch + HydrationBoundary (Connect SSR + Client Cache)

Prefetch data in Server Component and hydrate to Client Component.
Without this pattern, Client Component starts fetch from scratch after mount, causing loading flicker.

```tsx
// app/(routes)/users/page.tsx — Server Component
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import { UserList } from './_components/UserList';

export default async function UsersPage() {
  const queryClient = new QueryClient();

  // Prefetch on server — queryKey must be identical to Client
  await queryClient.prefetchQuery({
    queryKey: ['users'],
    queryFn: getUsers,
  });

  return (
    // Pass dehydrated cache to client
    <HydrationBoundary state={dehydrate(queryClient)}>
      <UserList />   {/* Renders immediately without loading since cache exists */}
    </HydrationBoundary>
  );
}
```

```tsx
// app/(routes)/users/_components/UserList.tsx — Client Component
'use client';

export function UserList() {
  // isLoading starts as false since prefetched data is in cache
  const { data: users } = useQuery({
    queryKey: ['users'],              // Must match server's prefetchQuery key
    queryFn: getUsers,
  });

  return (
    <ul>
      {users?.map((user) => <UserCard key={user.id} user={user} />)}
    </ul>
  );
}
```

> ⚠️ If `prefetchQuery`'s `queryKey` differs from Client's `useQuery` `queryKey`, hydration won't connect and server fetch results are discarded.

### 2-5. useQuery — Client Component Data Fetching

```typescript
// src/hooks/useUser.ts
import { useQuery } from '@tanstack/react-query';
import { getUser } from '@/lib/api/users';

export function useUser(userId: number) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => getUser(userId),   // Function from src/lib/api/users.ts
    staleTime: 1000 * 60 * 5,        // 5 minutes (override global default)
  });
}
```

- Prohibit direct `fetch()` or `apiClient` calls inside `useEffect` — must use TanStack Query
- Prohibit storing server state (API responses) in Zustand

### 2-6. useMutation — Server Data Mutation

All create/update/delete operations use `useMutation`.
Prohibit managing `isPending`, `onSuccess`, `onError` directly with `useState`.

```typescript
// src/hooks/useCreateUser.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api/users';

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserRequest) => userApi.create(data),
    onSuccess: () => {
      // Invalidate related cache on success — list auto-updates
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('User created.');
    },
    onError: (error: ApiError) => {
      toast.error(error.message);
    },
  });
}
```

```tsx
// React Hook Form + useMutation connection pattern
'use client';

export function CreateUserForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<CreateUserRequest>({
    resolver: zodResolver(createUserSchema),
  });

  const { mutate: createUser, isPending } = useCreateUser();

  return (
    // handleSubmit validates then calls mutate
    <form onSubmit={handleSubmit((values) => createUser(values))}>
      <input {...register('email')} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

- `mutationFn` must use functions from `src/lib/api/{domain}.ts`
- Must invalidate related cache in `onSuccess` with `invalidateQueries`
- Prohibit managing `isPending` state with separate `useState` — use `useMutation`'s `isPending`

---

## 3. Component Writing Rules

### 3-1. Basic Format

```tsx
// ✅ named export + separate Props interface
// Must declare 'use client' since using Client Hook (useUser)
'use client';

interface UserCardProps {
  userId: number;
  variant?: 'compact' | 'full';
}

export function UserCard({ userId, variant = 'full' }: UserCardProps) {
  const { data: user, isLoading } = useUser(userId);

  if (isLoading) return <UserCardSkeleton />;
  if (!user) return null;

  return <div className={cn(userCardVariants({ variant }))}>{user.name}</div>;
}
```

### 3-2. Server Component vs Client Component

- Default is **Server Component** — only declare `'use client'` when necessary
- Need `'use client'` for: event handlers, `useState`, `useEffect`, browser APIs, TanStack Query hooks
- Push `'use client'` to lowest level in tree — keep parent as Server Component

```
✅ Correct structure:              ❌ Wrong structure:
ServerPage                        'use client' Page
  └─ ServerSection                  └─ ServerSection
       └─ 'use client' Button            └─ 'use client' Button
                                              (entire page loses RSC benefits)
```

### 3-3. Streaming with Suspense

Async Server Components must be wrapped with `<Suspense>` to enable streaming.
Don't await all fetches at the top — this blocks entire initial rendering.

```tsx
// ✅ Each section streams independently — sent sequentially as ready
export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection />          {/* Async Server Component */}
      </Suspense>
      <Suspense fallback={<FeedSkeleton />}>
        <ActivityFeed />          {/* Async Server Component */}
      </Suspense>
    </div>
  );
}
```

### 3-4. Memoization Criteria

By default, don't apply memoization — only use when measured performance issues exist.

| API | When to Use |
|-----|-------------|
| `React.memo` | Frequently re-renders with same props and rendering cost is high |
| `useMemo` | Truly expensive computations (e.g., sorting/filtering large lists) |
| `useCallback` | Passing functions as props to memoized child components |

### 3-5. Component Size

- Split into sub-components if over 100 lines
- One component should have one responsibility

---

## 4. API Integration Rules

### 4-1. API Client (Client-Side)

```typescript
// src/lib/api/client.ts
export class ApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<ApiResponse<T>> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json();
    throw new ApiError(error.error.code, error.error.message, res.status);
  }

  return res.json();
}
```

### 4-2. API Function Location

- Client-side functions: `src/lib/api/{domain}.ts`
- Prohibit direct `fetch()` calls inside components or hooks

### 4-3. Response Type Definition

Mirror BE schemas directly in `src/types/api/{domain}.ts`.

```typescript
// src/types/api/user.ts
export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: { code: string; message: string } | null;
}

export interface User {
  id: number;
  email: string;
  name: string;
  isActive: boolean;
  createdAt: string;
}
```

---

## 5. Form Handling

All forms use **React Hook Form + Zod + useMutation** combination.
Prohibit managing form state or loading state with `useState`.

```tsx
// src/hooks/useLogin.ts — useMutation must be separated into custom hook
// Hook file doesn't need 'use client' — component using this hook needs 'use client'
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';

export function useLogin() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: (values: LoginFormValues) => authApi.login(values),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['me'] });
      router.push('/dashboard');
    },
    onError: (error: ApiError) => {
      toast.error(error.message);
    },
  });
}
```

```tsx
// src/components/features/auth/LoginForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email format.'),
  password: z.string().min(8, 'Password must be at least 8 characters.'),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  // useMutation separated into custom hook — queryClient/router declared inside hook
  const { mutate: login, isPending } = useLogin();

  return (
    <form onSubmit={handleSubmit((values) => login(values))}>
      <input {...register('email')} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      <input type="password" {...register('password')} />
      {errors.password && <p role="alert">{errors.password.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

---

## 6. State Management Rules

| State Type | Tool | Example |
|-----------|------|---------|
| Server state (API responses) | TanStack Query | User profile, product list |
| Shareable UI state (filters, tabs, page) | URL state (`useSearchParams` / `nuqs`) | `?page=2&sort=asc` |
| Client global state (auth, theme) | Zustand | Login session |
| Local UI state | `useState` | Modal open/close |

- Prohibit storing server state in Zustand — that's TanStack Query's role
- UI state needing bookmarks or sharing must be stored in URL

### Zustand Store Pattern

```typescript
// src/stores/authStore.ts
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  setUser: (user: User | null) => void;
  clearUser: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));

// ✅ Use selector to prevent unnecessary re-renders
export const useCurrentUser = () => useAuthStore((state) => state.user);
```

---

## 7. Declarative Coding First

Write in declarative (what) rather than imperative (how) style to improve readability and maintainability.
Express conditions, list processing, and render branching declaratively.

### 7-1. Conditional Rendering

```tsx
// ❌ Imperative — becomes harder to read as conditions grow
function UserStatus({ user }: { user: User }) {
  let badge;
  if (user.role === 'admin') {
    badge = <AdminBadge />;
  } else if (user.isActive) {
    badge = <ActiveBadge />;
  } else {
    badge = <InactiveBadge />;
  }
  return <div>{badge}</div>;
}

// ✅ Declarative — intent clear at a glance with component map
// Map component itself, not JSX instance — safely extensible when props are added
const statusBadgeMap: Record<string, React.ComponentType> = {
  admin: AdminBadge,
  active: ActiveBadge,
  inactive: InactiveBadge,
};

function UserStatus({ user }: { user: User }) {
  const key = user.role === 'admin' ? 'admin' : user.isActive ? 'active' : 'inactive';
  const Badge = statusBadgeMap[key];
  return <div><Badge /></div>;
}
```

### 7-2. List Processing

```tsx
// ❌ Imperative
function ActiveUserList({ users }: { users: User[] }) {
  const result = [];
  for (const user of users) {
    if (user.isActive) {
      result.push(<UserCard key={user.id} user={user} />);
    }
  }
  return <ul>{result}</ul>;
}

// ✅ Declarative
function ActiveUserList({ users }: { users: User[] }) {
  const activeUsers = users.filter((user) => user.isActive);

  return (
    <ul>
      {activeUsers.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </ul>
  );
}
```

### 7-3. Loading/Error/Empty State Branching

```tsx
// ❌ Inline branching — JSX becomes complex
function UserProfile({ userId }: { userId: number }) {
  const { data, isLoading, isError } = useUser(userId);
  return (
    <div>
      {isLoading ? <Spinner /> : isError ? <ErrorMessage /> : !data ? <EmptyState /> : <ProfileCard user={data} />}
    </div>
  );
}
```

```tsx
// ✅ Declarative early return — each state clearly separated
// 'use client' must be at top of file
'use client';

function UserProfile({ userId }: { userId: number }) {
  const { data: user, isLoading, isError } = useUser(userId);

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage />;
  if (!user) return <EmptyState />;

  return <ProfileCard user={user} />;
}
```

### 7-4. Event Handlers

```tsx
// ❌ Inline logic in JSX
<button onClick={() => {
  if (!isLoading) {
    setCount(count + 1);
    track('button_clicked');
  }
}}>
  Click
</button>

// ✅ Separate into handler with meaningful name
function handleClick() {
  if (isLoading) return;
  setCount((prev) => prev + 1);
  track('button_clicked');
}

<button onClick={handleClick}>Click</button>
```

---

## 8. TypeScript Rules

- `strict: true` mandatory in `tsconfig.json`
- Prohibit `any` type (if unavoidable: `// eslint-disable-next-line @typescript-eslint/no-explicit-any` + reason comment)
- Prohibit `// @ts-ignore` — allow `// @ts-expect-error` + reason comment
- Criteria for `interface` vs `type`:
  - Object shape → `interface`
  - Union / Intersection / Primitive alias / Function signature → `type`
- Type specification mandatory for all component Props
- Use Zod schema as single source for form and API validation types

```typescript
// ✅ Derive TypeScript type from Zod schema — prohibit duplicate definition
const userSchema = z.object({ id: z.number(), name: z.string() });
type User = z.infer<typeof userSchema>;
```

---

## 9. Performance

### 9-1. Images

Must use `next/image`. Prohibit plain `<img>` tag.

```tsx
import Image from 'next/image';

// ✅ Fixed-size image
<Image src="/hero.png" alt="Hero image" width={1200} height={600} priority />

// ✅ Use fill mode when size unknown
<div className="relative h-64 w-full">
  <Image src={user.avatar} alt={user.name} fill className="object-cover" />
</div>
```

- Add `priority` to above-the-fold images (LCP elements)
- Always provide meaningful `alt` text

### 9-2. Fonts

Must use `next/font`. Prohibit loading fonts via `<link>` or `@import`.

```typescript
// src/app/layout.tsx — Final version including both AppProviders and font
import { Inter } from 'next/font/google';
import { AppProviders } from './providers';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // Must apply inter.variable for font to actually be used
    <html lang="en" className={inter.variable}>
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
```

### 9-3. Dynamic Import

Lazy-load heavy components not needed for initial render.

```typescript
// ✅ Heavy chart library — unnecessary until tab opened
const Chart = dynamic(() => import('@/components/features/analytics/Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,         // Browser-only library
});
```

### 9-4. Bundle Size

- Prohibit importing entire library when only one function needed
- Check bundle impact with `@next/bundle-analyzer` before adding new dependencies

```typescript
// ❌
import _ from 'lodash';
const sorted = _.sortBy(items, 'name');

// ✅
import sortBy from 'lodash/sortBy';
const sorted = sortBy(items, 'name');
```

### 9-5. Script Loading

```tsx
import Script from 'next/script';

// ✅ Prevent third-party scripts from blocking render
<Script src="https://analytics.example.com/script.js" strategy="lazyOnload" />
```

---

## 10. SEO and Metadata

All pages must export metadata. Don't leave `<title>` or OG tags empty.

```typescript
// Static metadata
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: { title: 'Page Title', description: 'Page description' },
};

// Dynamic metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.id);
  return {
    title: product.name,
    openGraph: { images: [product.imageUrl] },
  };
}
```

---

## 11. Environment Variable Management

| Prefix | Accessible From | Purpose |
|--------|----------------|---------|
| `NEXT_PUBLIC_` | Browser + Server | Public API URL, feature flags |
| (no prefix) | Server only | Secret keys, internal API URLs |

```bash
# .env.example — List keys only, no values. Commit only this file to git
NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_GA_ID=
API_SECRET_KEY=
```

- Prohibit `NEXT_PUBLIC_` prefix for secret environment variables
- Add `.env*.local` to `.gitignore`, commit only `.env.example`
- Access environment variables through typed constants file — detect missing vars at startup

```typescript
// src/constants/env.ts
export const env = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL!,
  gaId: process.env.NEXT_PUBLIC_GA_ID,
} as const;
```

---

## 12. Naming Conventions

| Target | Rule | Example |
|--------|------|---------|
| Component files | PascalCase | `UserCard.tsx` |
| Hook files | camelCase, `use` prefix | `useUserProfile.ts` |
| Util files | camelCase | `formatDate.ts` |
| Store files | camelCase, `Store` suffix | `authStore.ts` |
| Types/Interfaces | PascalCase | `UserProfile` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| Route-local components | `_components/` prefix folder | `_components/HeroSection.tsx` |
| Path alias | Map `@/` to `src/` | `import { Button } from '@/components/ui/Button'` |

---

## 13. Styling

- Use **Tailwind CSS only** — prohibit inline `style` attribute (except dynamic values not expressible in Tailwind)
- Use `clsx` or `cn()` for conditional classes — prohibit string concatenation
- Allow CSS Modules only for complex animations
- Prohibit hardcoded color hex values — always use Tailwind tokens

```tsx
// ❌
<div style={{ color: '#3b82f6' }} className={'card' + (active ? ' active' : '')} />

// ✅
<div className={cn('rounded-lg bg-white', { 'ring-2 ring-blue-500': active })} />
```

---

## 14. Error Handling

```tsx
// Page level: error.tsx (Next.js App Router)
'use client';
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div role="alert">
      <p>An error occurred.</p>
      <button onClick={reset}>Retry</button>
    </div>
  );
}

// Component level: conditional rendering or ErrorBoundary
// API errors: catch ApiError and show toast notification
try {
  await createUser(data);
} catch (error) {
  if (error instanceof ApiError) toast.error(error.message);
  else throw error;               // Must re-throw unexpected errors
}
```

---

## 15. Accessibility (a11y)

- `alt` mandatory for all images (decorative images: `alt=""`)
- All interactive elements (`button`, `a`) must have text content or accessible label via `aria-label`
- Prohibit indicating state with color alone — combine with icon or text
- Form error messages must have `role="alert"` for screen reader announcement
- Verify keyboard navigation works without mouse — validate with Tab key
- Mandatory focus management when modal opens/closes (`focus-trap`, `autoFocus`)
- Minimum touch target size: 44×44px

---

## 16. Barrel Export (`index.ts`)

`index.ts` barrel files can be used limitedly to simplify imports, but follow strict rules to preserve tree-shaking.

```typescript
// ✅ Re-export few items within one domain — allowed
// src/components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';

// ❌ Prohibited — cross-domain re-export or entire directory export
// Breaks tree-shaking and creates circular dependency risk
export * from '../features';
export * from '../hooks';
```

---

## 17. Prohibited Actions (Complete Summary)

| Prohibited Item | Alternative |
|-----------------|-------------|
| `console.log()` in committed code | Remove before commit or use logger utility |
| `// @ts-ignore` | `// @ts-expect-error` + reason comment |
| `any` type | Explicit type; if unavoidable `// eslint-disable` + reason |
| `default export` | named export (except Next.js page/layout files) |
| API calls in `useEffect` | TanStack Query (`useQuery` / `useMutation`) |
| Hardcoded API URLs | `env` constants via environment variables |
| `<img>` tag | `next/image` |
| `<link>` / `@import` font loading | `next/font` |
| `style={{ ... }}` | Tailwind classes |
| String class concatenation | `cn()` / `clsx()` |
| Store server state in Zustand | TanStack Query |
| Manage shareable UI state with `useState` | URL state (`useSearchParams` / `nuqs`) |
| Manage form/loading state with `useState` | React Hook Form + Zod + `useMutation` |
| Missing cache invalidation after mutation success | Call `invalidateQueries` in `onSuccess` |
| `QueryClientProvider` directly in `layout.tsx` | Separate into `providers.tsx` |
| Declare `new QueryClient()` directly at component top | `useState(() => new QueryClient())` pattern |
| Mismatch between `prefetchQuery` and `useQuery` `queryKey` | Must use identical key |
| Inline complex logic in JSX | Separate into meaningful handler/variable names |
| Await all fetches before render | Suspense + streaming |
| Import entire library | named / path import |
| `NEXT_PUBLIC_` prefix for secrets | No-prefix server-only environment variables |
| `export *` in barrel files (cross-domain) | Explicit named re-export |
