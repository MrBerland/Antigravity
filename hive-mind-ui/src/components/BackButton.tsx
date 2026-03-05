'use client';

import { useRouter } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';

export default function BackButton() {
    const router = useRouter();

    return (
        <button
            onClick={() => router.back()}
            className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 transition-colors"
            title="Go Back"
        >
            <ArrowLeft size={20} />
        </button>
    );
}
