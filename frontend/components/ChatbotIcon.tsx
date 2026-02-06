'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';

const ChatbotIcon = ({ onOpen }) => {
  const [isVisible, setIsVisible] = useState(true);
  const [isHovered, setIsHovered] = useState(false);

  // Check if user is logged in by checking for auth token in localStorage
  const isLoggedIn = () => {
    if (typeof window !== 'undefined') {
      return !!localStorage.getItem('auth-token') || !!localStorage.getItem('better-auth-session');
    }
    return false;
  };

  // Only show the icon if user is logged in
  if (!isLoggedIn()) {
    return null;
  }

  return (
    <motion.div
      className={`fixed bottom-6 right-6 z-50 cursor-pointer ${
        isVisible ? 'opacity-100' : 'opacity-0'
      }`}
      initial={{ scale: 0 }}
      animate={{ scale: isHovered ? 1.1 : 1 }}
      whileTap={{ scale: 0.95 }}
      onClick={onOpen}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative">
        {/* Pulse animation for new messages */}
        <div className="absolute -inset-2 bg-blue-500 rounded-full opacity-75 animate-ping"></div>

        {/* Chat icon */}
        <div className="bg-blue-600 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clipRule="evenodd" />
          </svg>
        </div>
      </div>
    </motion.div>
  );
};

export default ChatbotIcon;