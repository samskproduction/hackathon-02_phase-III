'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { apiClient } from '@/lib/api';

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatWindow = ({ isOpen, onClose }: ChatWindowProps) => {
  const [messages, setMessages] = useState([
    { id: 1, role: 'assistant', content: 'Hello! I\'m your AI assistant. How can I help you manage your tasks today?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Get user ID from local storage (stored during authentication)
  const getUserId = () => {
    if (typeof window !== 'undefined') {
      // Try multiple possible locations for user data
      let userDataStr = localStorage.getItem('user-data'); // This matches what's stored in the auth provider
      if (userDataStr) {
        try {
          const userData = JSON.parse(userDataStr);
          return userData.id || userData.sub || null;
        } catch {
          return null;
        }
      }

      // Fallback to other possible locations
      userDataStr = localStorage.getItem('better-auth.user');
      if (userDataStr) {
        try {
          const userData = JSON.parse(userDataStr);
          return userData.id || userData.sub || null;
        } catch {
          return null;
        }
      }
    }
    return null;
  };

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending a message
  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userId = getUserId();
    if (!userId) {
      setMessages(prev => [...prev, {
        id: Date.now(),
        role: 'assistant',
        content: 'Error: User not authenticated. Please log in to use the chat assistant.'
      }]);
      return;
    }

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API to process the message
      const response = await apiClient.chat(userId, inputValue, currentConversationId);

      if (response.success && response.data) {
        // Update the conversation ID if it was returned
        if (response.data.conversation_id && !currentConversationId) {
          setCurrentConversationId(response.data.conversation_id);
        }

        // Add the assistant response
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data.response
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.error?.message || 'Sorry, I encountered an error processing your request. Please try again.'
        };

        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error: any) {
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: error.message || 'Sorry, I encountered an error connecting to the server. Please try again.'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle key press (Enter to send)
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed bottom-24 right-6 z-50 w-[400px] h-[500px] flex flex-col bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden"
        initial={{ opacity: 0, y: 50, scale: 0.8 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 50, scale: 0.8 }}
        transition={{ type: 'spring', damping: 20, stiffness: 300 }}
      >
        {/* Header */}
        <div className="bg-blue-600 text-white p-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clipRule="evenodd" />
            </svg>
            <span className="font-semibold">AI Task Assistant</span>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-gray-200 focus:outline-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        {/* Messages container */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-900">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex mb-4 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-gray-600'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-gray-600 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
          <div className="flex items-end space-x-2">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg p-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              rows={1}
              style={{ minHeight: '40px', maxHeight: '100px' }}
            />
            <button
              onClick={handleSend}
              disabled={isLoading || !inputValue.trim()}
              className={`p-2 rounded-lg ${
                isLoading || !inputValue.trim()
                  ? 'bg-gray-300 dark:bg-gray-600 text-gray-500'
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              }`}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export default ChatWindow;