// frontend/lib/better-auth-client.ts
import { createAuthClient } from 'better-auth/client';

export const betterAuthClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8000', // This should match your backend URL
});