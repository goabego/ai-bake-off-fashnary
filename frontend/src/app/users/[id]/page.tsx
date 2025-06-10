import React, { Suspense } from 'react';
import { notFound } from 'next/navigation';
import { Badge } from '@/components/ui/badge';

async function getUser(id: string) {
  const res = await fetch(`http://localhost:8000/users/${id}/display`);
  if (!res.ok) return null;
  return res.json();
}

export default async function UserProfilePage({ params }: { params: { id: string } }) {
  const user = await getUser(params.id);
  if (!user) return notFound();

  return (
    <div className="max-w-2xl mx-auto py-10 px-4">
      <div className="flex flex-col items-center gap-4">
        <img
          src={user.image}
          alt={user.name}
          className="w-80 h-80 rounded-full object-cover border-4 border-primary shadow-lg"
        />
        <p>{user.image_url}</p>
        <h1 className="text-3xl font-bold text-center">{user.name}</h1>
        <div className="flex flex-wrap gap-2 mb-4">Preferences: 
          {user.style_preferences.map((pref: string) => (
            <Badge key={pref} variant="secondary">{pref}</Badge>
          ))}
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-2">Purchase History</h2>
        {user.purchase_history.length > 0 ? (
          <ul className="list-disc list-inside text-gray-700">
            {user.purchase_history.map((pid: string) => (
              <li key={pid}>Product ID: <span className="font-mono">{pid}</span></li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-400">No purchases yet.</p>
        )}
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-2">Current Cart</h2>
        {user.cart_status && user.cart_status.items.length > 0 ? (
          <div className="bg-gray-50 rounded-lg p-4 shadow">
            <ul className="divide-y divide-gray-200">
              {user.cart_status.items.map((item: any, idx: number) => (
                <li key={idx} className="py-2 flex justify-between">
                  <span>Product ID: <span className="font-mono">{item.product_id}</span></span>
                  <span>Qty: {item.quantity}</span>
                </li>
              ))}
            </ul>
            <div className="mt-2 text-right font-semibold">
              Total: ${user.cart_status.total_price.toFixed(2)}
            </div>
          </div>
        ) : (
          <p className="text-gray-400">Cart is empty.</p>
        )}
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-2">Full User JSON</h2>
        <pre className="bg-gray-900 text-gray-100 rounded-lg p-4 text-xs overflow-x-auto">
          {JSON.stringify(user, null, 2)}
        </pre>
      </div>
    </div>
  );
} 