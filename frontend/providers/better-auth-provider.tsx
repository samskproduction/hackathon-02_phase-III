'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { UserSession } from '@/lib/types';
import { apiClient } from '@/lib/api';

interface AuthContextType {
  user: UserSession | null;
  isAuthenticated: boolean;
  login: (credentials: { email: string; password: string }) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function BetterAuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session on mount
    const token = localStorage.getItem('better-auth-session');
    if (token) {
      // In a real implementation, you would validate the token with the backend
      // For now, we'll assume it's valid and the user data is stored
      const userData = localStorage.getItem('user-data');
      if (userData) {
        try {
          const parsedUser = JSON.parse(userData);
          setUser(parsedUser);
        } catch (error) {
          console.error('Failed to parse user data:', error);
        }
      }
    }
    setLoading(false);
  }, []);

  const login = async (credentials: { email: string; password: string }) => {
    try {
      // Call our backend API for login
      const response = await apiClient.login(credentials.email, credentials.password);

      if (response.success && response.data) {
        // Store the session token
        localStorage.setItem('better-auth-session', response.data.token);
        localStorage.setItem('user-data', JSON.stringify(response.data.user));
        setUser(response.data.user);
      } else {
        throw new Error(response.error?.message || 'Login failed');
      }
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      // Call our backend API for logout
      await apiClient.logout();

      // Clear local storage
      localStorage.removeItem('better-auth-session');
      localStorage.removeItem('user-data');
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
      // Still clear local storage even if API call fails
      localStorage.removeItem('better-auth-session');
      localStorage.removeItem('user-data');
      setUser(null);
    }
  };

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    logout,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within a BetterAuthProvider');
  }
  return context;
}