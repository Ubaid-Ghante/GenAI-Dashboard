// src/components/chat/WidgetRenderer.tsx
interface Widget {
    type: string;
    data: any;
    title: string;
    options?: object;
}

interface WidgetRendererProps {
    widget: Widget;
}

export default function WidgetRenderer({ widget }: WidgetRendererProps) {
    // For now, we'll just display the widget data as JSON
    // In a real implementation, you would render actual charts using a library like Chart.js
    return (
        <div className="bg-gray-100 p-3 rounded border">
            <h4 className="font-medium text-gray-800 mb-2">{widget.title}</h4>
            <pre className="text-xs bg-white p-2 rounded overflow-auto max-h-40">
                {JSON.stringify(widget.data, null, 2)}
            </pre>
            <p className="text-xs text-gray-500 mt-1">Widget type: {widget.type}</p>
        </div>
    );
}
