// src/components/chat/ChatMessages.tsx
import { Message } from '@/app/chat/page';
import ChatMessage from './ChatMessage';

interface ChatMessagesProps {
    messages: Message[];
}

export default function ChatMessages({ messages }: ChatMessagesProps) {
    return (
        <div className="h-full overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
            ))}
        </div>
    );
}
