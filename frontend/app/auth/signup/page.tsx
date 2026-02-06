import { SignupForm } from '@/components/auth/signup-form';

export default function SignupPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Join TodoApp</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">Create an account to get started</p>
        </div>
        <SignupForm />
      </div>
    </div>
  );
}