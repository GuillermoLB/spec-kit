# Feature: Frontend Plugin

**Status**: Draft
**Owner**: spec-kit development team
**Last Updated**: 2026-01-17
**Priority**: Low

## Purpose

Create a frontend development plugin providing React and TypeScript patterns, state management strategies, API integration best practices, and modern frontend tooling configurations. This plugin helps frontend developers build scalable React applications.

## Requirements

- [ ] SKILL.md with React and TypeScript patterns
- [ ] TypeScript configuration templates (tsconfig.json)
- [ ] React component templates (functional components with hooks)
- [ ] State management examples (Context API, custom hooks)
- [ ] API client integration patterns
- [ ] Form handling and validation examples
- [ ] React Router patterns
- [ ] Testing templates (React Testing Library)
- [ ] Build tool configuration (Vite)
- [ ] Integration with install.sh
- [ ] Validation in verify.sh

## User Stories

**As a** frontend developer
**I want** React and TypeScript patterns
**So that** I can build type-safe, maintainable React applications

**As a** full-stack developer
**I want** API integration patterns
**So that** I can connect my React frontend to backend APIs effectively

**As a** team lead
**I want** consistent frontend patterns
**So that** my team follows best practices for React development

## Acceptance Criteria

1. **Given** I install the frontend plugin
   **When** I check .claude/skills/frontend/
   **Then** I see SKILL.md and template files

2. **Given** I use React component templates
   **When** I create components
   **Then** I have properly typed components with hooks

3. **Given** I use API client templates
   **When** I integrate with backend APIs
   **Then** I have type-safe API calls with error handling

4. **Given** I use form templates
   **When** I build forms
   **Then** I have validation and error display

5. **Given** I use testing templates
   **When** I write component tests
   **Then** I follow React Testing Library best practices

## Technical Details

### Plugin Structure

```
plugins/frontend/
├── skill.md                       # Main plugin file
└── templates/
    ├── config/
    │   ├── tsconfig.json          # TypeScript configuration
    │   ├── vite.config.ts         # Vite configuration
    │   └── .eslintrc.js           # ESLint configuration
    ├── components/
    │   ├── Button.tsx             # Component example
    │   ├── Form.tsx               # Form component
    │   └── DataTable.tsx          # Data table with pagination
    ├── hooks/
    │   ├── useApi.ts              # API hook
    │   ├── useForm.ts             # Form hook
    │   └── useLocalStorage.ts    # Local storage hook
    ├── api/
    │   ├── client.ts              # API client
    │   └── types.ts               # API types
    ├── context/
    │   └── AuthContext.tsx        # Context example
    └── tests/
        ├── Button.test.tsx        # Component test
        └── setup.ts               # Test setup
```

### TypeScript Configuration

**Template: tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,

    /* Path mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@hooks/*": ["src/hooks/*"],
      "@utils/*": ["src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### React Component Templates

**Template: components/Button.tsx**

```typescript
/**
 * Reusable Button component with variants.
 */
import React from 'react';

interface ButtonProps {
  /** Button text */
  children: React.ReactNode;
  /** Button variant */
  variant?: 'primary' | 'secondary' | 'danger';
  /** Button size */
  size?: 'small' | 'medium' | 'large';
  /** Disabled state */
  disabled?: boolean;
  /** Loading state */
  loading?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Button type */
  type?: 'button' | 'submit' | 'reset';
  /** CSS class name */
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
  className = '',
}) => {
  const baseClasses = 'btn';
  const variantClasses = `btn-${variant}`;
  const sizeClasses = `btn-${size}`;
  const stateClasses = disabled || loading ? 'btn-disabled' : '';

  const classes = [baseClasses, variantClasses, sizeClasses, stateClasses, className]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled || loading}
      aria-busy={loading}
    >
      {loading ? (
        <>
          <span className="spinner" aria-hidden="true" />
          <span className="sr-only">Loading...</span>
        </>
      ) : (
        children
      )}
    </button>
  );
};
```

**Template: components/Form.tsx**

```typescript
/**
 * Form component with validation.
 */
import React, { useState } from 'react';

interface FormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
}

interface LoginFormProps {
  onSubmit: (data: FormData) => Promise<void>;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user types
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
    } catch (error) {
      setErrors({ email: 'Invalid credentials' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          className={errors.email ? 'input-error' : ''}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <span id="email-error" className="error-message" role="alert">
            {errors.email}
          </span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          className={errors.password ? 'input-error' : ''}
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
        {errors.password && (
          <span id="password-error" className="error-message" role="alert">
            {errors.password}
          </span>
        )}
      </div>

      <Button type="submit" loading={isSubmitting} disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Log in'}
      </Button>
    </form>
  );
};
```

### Custom Hooks

**Template: hooks/useApi.ts**

```typescript
/**
 * Custom hook for API calls with loading and error states.
 */
import { useState, useCallback } from 'react';

interface UseApiOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

interface UseApiReturn<T, P extends any[]> {
  data: T | null;
  error: Error | null;
  loading: boolean;
  execute: (...args: P) => Promise<void>;
  reset: () => void;
}

export function useApi<T, P extends any[]>(
  apiFunction: (...args: P) => Promise<T>,
  options: UseApiOptions<T> = {}
): UseApiReturn<T, P> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(false);

  const execute = useCallback(
    async (...args: P) => {
      setLoading(true);
      setError(null);

      try {
        const result = await apiFunction(...args);
        setData(result);
        options.onSuccess?.(result);
      } catch (err) {
        const error = err instanceof Error ? err : new Error('Unknown error');
        setError(error);
        options.onError?.(error);
      } finally {
        setLoading(false);
      }
    },
    [apiFunction, options]
  );

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return { data, error, loading, execute, reset };
}

// Usage example
/*
const { data, error, loading, execute } = useApi(fetchUsers);

useEffect(() => {
  execute();
}, [execute]);
*/
```

**Template: hooks/useForm.ts**

```typescript
/**
 * Custom hook for form handling with validation.
 */
import { useState, useCallback } from 'react';

type ValidationRule<T> = (value: T) => string | undefined;
type ValidationRules<T> = Partial<Record<keyof T, ValidationRule<T[keyof T]>>>;

interface UseFormOptions<T> {
  initialValues: T;
  validationRules?: ValidationRules<T>;
  onSubmit: (values: T) => void | Promise<void>;
}

export function useForm<T extends Record<string, any>>({
  initialValues,
  validationRules = {},
  onSubmit,
}: UseFormOptions<T>) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = useCallback(() => {
    const newErrors: Partial<Record<keyof T, string>> = {};

    Object.keys(validationRules).forEach((key) => {
      const fieldKey = key as keyof T;
      const rule = validationRules[fieldKey];
      if (rule) {
        const error = rule(values[fieldKey]);
        if (error) {
          newErrors[fieldKey] = error;
        }
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [values, validationRules]);

  const handleChange = useCallback((name: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [name]: value }));
    setTouched(prev => ({ ...prev, [name]: true }));
  }, []);

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();

      // Mark all fields as touched
      const allTouched = Object.keys(values).reduce(
        (acc, key) => ({ ...acc, [key]: true }),
        {} as Partial<Record<keyof T, boolean>>
      );
      setTouched(allTouched);

      if (!validate()) return;

      setIsSubmitting(true);
      try {
        await onSubmit(values);
      } finally {
        setIsSubmitting(false);
      }
    },
    [values, validate, onSubmit]
  );

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleSubmit,
    reset,
  };
}
```

### API Client Template

**Template: api/client.ts**

```typescript
/**
 * Type-safe API client.
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public response?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

class ApiClient {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  setAuthToken(token: string | null) {
    if (token) {
      this.defaultHeaders['Authorization'] = `Bearer ${token}`;
    } else {
      delete this.defaultHeaders['Authorization'];
    }
  }

  private async request<T>(
    method: string,
    endpoint: string,
    data?: any
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const options: RequestInit = {
      method,
      headers: this.defaultHeaders,
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || 'Request failed',
          response.status,
          errorData
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError('Network error', 0, error);
    }
  }

  get<T>(endpoint: string): Promise<T> {
    return this.request<T>('GET', endpoint);
  }

  post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>('POST', endpoint, data);
  }

  put<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>('PUT', endpoint, data);
  }

  delete<T>(endpoint: string): Promise<T> {
    return this.request<T>('DELETE', endpoint);
  }
}

export const apiClient = new ApiClient();

// Usage example with types
/*
interface User {
  id: string;
  name: string;
  email: string;
}

const getUser = (id: string) => apiClient.get<User>(`/users/${id}`);
const createUser = (data: Omit<User, 'id'>) => apiClient.post<User>('/users', data);
*/
```

### Context Template

**Template: context/AuthContext.tsx**

```typescript
/**
 * Authentication context with React Context API.
 */
import React, { createContext, useContext, useState, useCallback } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    try {
      // Call your login API
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) throw new Error('Login failed');

      const data = await response.json();
      setUser(data.user);
      localStorage.setItem('token', data.token);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem('token');
  }, []);

  const value: AuthContextValue = {
    user,
    isAuthenticated: !!user,
    login,
    logout,
    isLoading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### Testing Template

**Template: tests/Button.test.tsx**

```typescript
/**
 * Component tests with React Testing Library.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from '../components/Button';

describe('Button', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('shows loading state', () => {
    render(<Button loading>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('applies variant classes', () => {
    render(<Button variant="danger">Delete</Button>);
    expect(screen.getByRole('button')).toHaveClass('btn-danger');
  });
});
```

### Security Considerations

- [ ] XSS prevention (React escapes by default)
- [ ] CSRF token handling for API requests
- [ ] Secure authentication token storage
- [ ] Input sanitization for user data
- [ ] Content Security Policy headers
- [ ] HTTPS for all API calls

## Edge Cases & Error Handling

1. **Edge case**: API returns 401 Unauthorized
   - **Handling**: Clear auth token, redirect to login

2. **Edge case**: Network request fails
   - **Handling**: Show error message, provide retry option

3. **Error**: TypeScript type mismatch
   - **Message**: Clear type error from TypeScript compiler
   - **Recovery**: Fix type definitions

## Testing Strategy

### Validation Tests

- [ ] Verify SKILL.md has valid YAML frontmatter
- [ ] Verify TypeScript templates compile without errors
- [ ] Verify JSON configurations are valid

### Manual Testing

- [ ] Use component templates in React project
- [ ] Verify hooks work as expected
- [ ] Test API client with real backend
- [ ] Run component tests

## Dependencies

- **Blocked by**: documentation-improvements
- **Blocks**: None
- **Related**: None (independent frontend focus)

## Implementation Notes

### Decisions Made

- 2026-01-17 - Focus on React (most popular frontend framework)
- 2026-01-17 - TypeScript required (industry standard)
- 2026-01-17 - Functional components with hooks (modern React)
- 2026-01-17 - React Testing Library (recommended testing approach)
- 2026-01-17 - Vite as build tool (fast, modern)

### Integration with install.sh

Add to plugin selection:

```bash
6) Frontend Plugin - React, TypeScript, hooks patterns
```

Update verify.sh:

```bash
echo "Plugin: frontend"
check_file "plugins/frontend/skill.md"
check_file "plugins/frontend/templates/config/tsconfig.json"
check_file "plugins/frontend/templates/components/Button.tsx"
```

## References

- React documentation: https://react.dev/
- TypeScript: https://www.typescriptlang.org/
- React Testing Library: https://testing-library.com/react
- Vite: https://vitejs.dev/

---

**Template Version**: 1.0
**Last Updated**: 2026-01-17
