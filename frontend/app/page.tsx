"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to signup as default starting point
    router.push("/signup");
  }, [router]);

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center">
      <div className="animate-pulse flex flex-col items-center gap-4">
        <div className="w-12 h-12 bg-gray-800 rounded-xl"></div>
        <p className="text-gray-500 font-bold">Loading TodoPro...</p>
      </div>
    </div>
  );
}
