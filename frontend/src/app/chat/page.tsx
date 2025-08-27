'use client';

import { useState } from 'react';
import ChatMessages from '@/components/chat/ChatMessages';
import ChatInput from '@/components/chat/ChatInput';

export interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    widget?: {
        type: string;
        data: any;
        title: string;
        options?: object;
    };
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);

    const handleSendMessage = async (content: string) => {
        // Add user message
        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content,
        };

        setMessages(prev => [...prev, userMessage]);

        // Simulate AI response (will be replaced with actual API call)
        setTimeout(() => {
            const aiMessage: Message = {
                id: Date.now().toString(),
                role: 'assistant',
                content: 'Here is your requested data:',
                widget: {
                    type: 'line_chart',
                    data: {
                        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        datasets: [
                            {
                                label: 'Sales',
                                data: [12, 19, 3, 5, 2, 3],
                                borderColor: 'rgb(75, 192, 192)',
                            },
                        ],
                    },
                    title: 'Sales Data',
                },
            };
            setMessages(prev => [...prev, aiMessage]);
        }, 1000);
    };

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            <div className="flex-1 overflow-hidden">
                <ChatMessages messages={messages} />
            </div>
            <ChatInput onSendMessage={handleSendMessage} />
        </div>
    );
}