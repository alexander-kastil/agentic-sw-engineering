---
name: react-state-mgmt
description: Manage React state across projects using modern patterns. Use when setting up global state management, choosing between Redux Toolkit, Zustand, or Jotai, managing server state with React Query, implementing optimistic updates, handling form state, debugging state issues, or migrating from legacy Redux patterns.
---

# React State Management

Master modern state management patterns for React applications, from local component state to global stores, server state synchronization, and complex data flows.

## When to Use This Skill

Use this skill when you need to:

- Set up global state management in a React application
- Choose between Redux Toolkit, Zustand, Jotai, or React Query
- Manage server state with caching and synchronization
- Implement optimistic updates and rollback patterns
- Manage form state with validation and complex interactions
- Debug state-related mutations and performance issues
- Migrate from legacy Redux patterns to modern approaches
- Combine multiple state management solutions
- Create typed, scalable state architecture with TypeScript

## Prerequisites

Project requirements:

- React 16.8+ (hooks support required)
- TypeScript configured with strict mode
- Node.js 14+ with npm/yarn
- Selected state management library (Redux Toolkit, Zustand, Jotai, or React Query)
- Understanding of React hooks (useState, useReducer, useContext)

## Core Concepts

### State Categories

| Category     | Purpose                      | Solutions                        |
| ------------ | ---------------------------- | -------------------------------- |
| Local State  | Component-specific, UI state | useState, useReducer             |
| Global State | Shared across components     | Redux Toolkit, Zustand, Jotai    |
| Server State | Remote data, caching, sync   | React Query, SWR, RTK Query      |
| URL State    | Route parameters, search     | React Router, nuqs               |
| Form State   | Input values, validation     | React Hook Form, Formik, Zustand |

### Selection Criteria

Choose based on application complexity and data needs:

- Small app, simple state: Zustand or Jotai
- Large app, complex state: Redux Toolkit with slices
- Heavy server interaction: React Query + light client state
- Atomic/granular updates: Jotai with atom-based architecture
- Form-heavy application: React Hook Form + local Zustand state
- Mixed requirements: Zustand for client + React Query for server

## Architectural Patterns

### Pattern 1: Redux Toolkit with TypeScript

Use Redux Toolkit for large, complex applications with:

- Complex state interactions
- Time-travel debugging needs
- DevTools middleware integration
- Async thunks for API calls

Structure:

- store/index.ts: Configure store with slices
- store/slices/featureSlice.ts: Feature-specific reducers and actions
- Hooks at store/hooks.ts: Typed useAppDispatch and useAppSelector

Key practices:

- Define PayloadAction types explicitly
- Use createAsyncThunk for API calls
- Implement proper error states (idle, loading, succeeded, failed)
- Type all state slices with TypeScript interfaces

### Pattern 2: Zustand for Scalable State

Use Zustand for medium to large apps requiring:

- Simple, unopinionated store setup
- Slice-based organization
- API integration without middleware
- Optimized re-renders with selective subscriptions

Structure:

- store/slices/userSlice.ts: User state and actions
- store/slices/cartSlice.ts: Cart state and actions
- store/index.ts: Combine slices with type-safe hooks

Key practices:

- Use StateCreator pattern for scalable slices
- Create selector hooks to prevent unnecessary re-renders
- Combine stores with shallow merging
- Middleware support (persist, devtools) for advanced features

### Pattern 3: Jotai for Atomic State

Use Jotai for applications with:

- Fine-grained reactivity requirements
- Derived and computed atoms
- Async atom support with Suspense
- Dynamic atom creation

Structure:

- atoms/userAtoms.ts: Individual atoms and derived atoms
- atoms/cartAtoms.ts: Cart-related atoms
- Components use useAtom hook for read/write operations

Key practices:

- Keep atoms small and focused
- Use derived atoms for computed values (dont store derived data)
- Leverage atomWithStorage for persistence
- Use write-only atoms for actions
- Enable Suspense for async atoms

### Pattern 4: React Query for Server State

Use React Query (TanStack Query) to:

- Fetch and cache remote data
- Handle success/error states
- Implement stale-while-revalidate pattern
- Synchronize server state with UI

Structure:

- hooks/useUsers.ts: Query and mutation definitions
- hooks/queryKeys.ts: Query key factory for consistency
- Components use hooks with automatic lifecycle management

Key practices:

- Define queryKey factory for consistent query identification
- Set staleTime and gcTime appropriately (previously cacheTime)
- Use enabled option for conditional queries
- Implement optimistic updates with onMutate/onError/onSettled
- Keep query client accessible for invalidation

### Pattern 5: Combining Client and Server State

For real-world applications, combine approaches:

- Zustand (or Jotai) for UI client state (sidebar, modals, filters)
- React Query for server state (users, posts, data)
- React Hook Form for form state validation

Benefits:

- Separation of concerns
- Optimized re-renders per state type
- Clear data flow and debugging
- Reusable query logic

## Implementation Workflow

### 1. Define State Structure

Start by identifying state categories:

- What is local/component UI state?
- What is shared global state?
- What comes from a server/API?
- What URL patterns need to be reflected?

### 2. Choose State Management Solution

Decision tree:

- Is it server data? → React Query
- Does it affect many components? → Zustand or Redux Toolkit
- Does it require complex reactions? → Jotai
- Is it form input? → React Hook Form + light client state

### 3. Setup Store/Atoms

For Redux Toolkit:

- Create store/index.ts with configureStore
- Create slices in store/slices/
- Export typed hooks at store/hooks.ts

For Zustand:

- Create store/slices/feature.ts with StateCreator
- Combine in store/index.ts
- Export selector hooks for optimization

For Jotai:

- Create atoms/index.ts with atom definitions
- Create derived atoms for computed values
- Export atoms for use in components

For React Query:

- Create hooks/useFeature.ts with useQuery/useMutation
- Define queryKey factory
- Implement error handling and optimistic updates

### 4. Integrate Into Components

- Import typed hooks (Redux, Zustand) or atoms (Jotai)
- Use in functional components with proper TypeScript types
- Memoize selectors to prevent unnecessary re-renders
- Handle loading and error states

### 5. Test State Logic

- Test reducers/slices in isolation (Redux)
- Test mutations and query behavior (React Query)
- Test atom subscriptions (Jotai)
- Verify DevTools integration for debugging

### 6. Optimize Performance

- Use selectors to subscribe to specific parts of state
- Memoize components with React.memo if needed
- Implement proper staleTime and gcTime (React Query)
- Avoid storing derived data

## Best Practices

### Do

- Colocate state close to where its used
- Use selectors and custom hooks to prevent unnecessary re-renders
- Normalize server data to avoid duplication
- Type everything with TypeScript for safety
- Separate server state (React Query) from client state (Zustand)
- Implement proper loading and error states
- Use DevTools for debugging and time-travel

### Don't

- Over-globalize state; not everything needs global store
- Duplicate server state with local state; let React Query manage it
- Mutate state directly; always use immutable updates (Redux/Zustand handle this)
- Store derived/computed data; compute it instead
- Mix multiple state solutions for the same category of state
- Ignore TypeScript types; embrace strict mode
- Ignore stale state; set appropriate staleTime values

## Troubleshooting

| Issue                   | Solution                                                                                                 |
| ----------------------- | -------------------------------------------------------------------------------------------------------- |
| Unnecessary re-renders  | Use selectors (Redux), custom hooks (Zustand), or atom subscriptions (Jotai); avoid parent state changes |
| State not updating      | Verify action/reducer/setter was dispatched; check DevTools for state changes                            |
| Stale data displayed    | Increase staleTime in React Query; manually invalidate queries when needed                               |
| Cannot serialize state  | Redux Toolkit has serializableCheck; use middleware options to ignore certain actions                    |
| Memory leaks with async | Unsubscribe from query changes; Zustand and React Query handle cleanup automatically                     |
| TypeScript type errors  | Export RootState and AppDispatch types from store; use StateCreator generics for Zustand                 |
| DevTools not showing    | Enable devtools middleware; Redux, Zustand, and Jotai all include DevTools support                       |
| Query keys not matching | Use queryKey factory pattern; ensure consistent key structure across mutations and queries               |

## Migration Guide: Legacy Redux to Redux Toolkit

From old-style Redux action creators and reducers:

```typescript
// Before
const ADD_TODO = "ADD_TODO"
const addTodo = (text) => ({ type: ADD_TODO, payload: text })
function todosReducer(state = [], action) {
  switch(action.type) {
    case ADD_TODO:
      return [...state, { text: action.payload, completed: false }]
    default:
      return state
  }
}

// After - Redux Toolkit
const todosSlice = createSlice({
  name: "todos",
  initialState: [] as Todo[],
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      state.push({ text: action.payload, completed: false })
    }
  }
})
export const { addTodo } = todosSlice.actions
```

Key improvements:

- Less boilerplate (no action creators needed)
- Immer integration allows "mutation-like" syntax
- Better TypeScript support
- Built-in DevTools
- Slice-based organization

## References

- Redux Toolkit: https://redux-toolkit.js.org/
- Zustand: https://github.com/pmndrs/zustand
- Jotai: https://jotai.org/
- TanStack Query: https://tanstack.com/query
- Microsoft Learn: React state management patterns
