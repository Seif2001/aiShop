import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center flex-col space-y-4">
      <h1 className="text-3xl font-bold">Welcome to the AI Assistant App</h1>
      <div className="space-x-4">
        <Link to="/login" className="bg-blue-500 text-white px-4 py-2 rounded">Login</Link>
        <Link to="/signup" className="bg-green-500 text-white px-4 py-2 rounded">Signup</Link>
      </div>
    </div>
  );
}
