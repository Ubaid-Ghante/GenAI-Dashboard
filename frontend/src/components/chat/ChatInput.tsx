// src/components/chat/ChatInput.tsx
'use client';

import { useState } from 'react';

interface ChatInputProps {
    onSendMessage: (message: string) => void;
}

export default function ChatInput({ onSendMessage }: ChatInputProps) {
    const [message, setMessage] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (message.trim()) {
            onSendMessage(message);
            setMessage('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
            <div className="flex space-x-2">
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Ask a question about your data..."
                    className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                    Send
                </button>
            </div>
        </form>
    );
}
