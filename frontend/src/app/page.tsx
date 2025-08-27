
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-6">AI Dashboard</h1>
        <Link
          href="/chat"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Open Chat Interface
        </Link>
      </div>
    </div>
  );
}