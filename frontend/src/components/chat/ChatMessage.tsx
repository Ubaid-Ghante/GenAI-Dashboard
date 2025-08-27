// src/components/chat/ChatMessage.tsx
import { Message } from '@/app/chat/page';
import WidgetRenderer from './WidgetRenderer';

interface ChatMessageProps {
    message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
    const isAssistant = message.role === 'assistant';

    return (
        <div className={`flex ${isAssistant ? 'justify-start' : 'justify-end'}`}>
            <div
                className={`max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl rounded-lg p-4 ${isAssistant
                    ? 'bg-white border border-gray-200'
                    : 'bg-blue-600 text-white'
                    }`}
            >
                <p>{message.content}</p>
                {message.widget && (
                    <div className="mt-3">
                        <WidgetRenderer widget={message.widget} />
                        <button className="mt-2 bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded text-sm">
                            Save to Dashboard
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
