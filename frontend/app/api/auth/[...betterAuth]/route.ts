import { BetterAuthAdapter } from 'better-auth/adapter';
import { DrizzleAdapter } from '@better-auth/drizzle-adapter';
import { db } from '@/lib/db'; // You'll need to set up your database connection
import { betterAuth } from 'better-auth';

const adapter = DrizzleAdapter(db, {
  provider: 'pg', // or 'mysql', 'sqlite' based on your database
});

export const { GET, POST } = betterAuth({
  database: adapter,
  secret: process.env.BETTER_AUTH_SECRET || 'fallback-secret-for-development',
  emailAndPassword: {
    enabled: true,
  },
});