"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { LogIn, Mail, Lock, ArrowRight, Github } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

export default function SigninPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Set user and redirect
    setTimeout(() => {
      login(email.split('@')[0] || "User", email);
      router.push("/tasks");
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-4 font-sans perspective-1000">
      <div className="max-w-md w-full animate-in zoom-in-95 duration-700">
        {/* Logo */}
        <div className="flex justify-center mb-10 gap-3">
            <div className="w-12 h-12 bg-white rounded-[1.2rem] flex items-center justify-center text-[#0f172a] font-black shadow-[0_10px_0_rgb(226,232,240),0_20px_30px_rgba(0,0,0,0.5)] transform -rotate-3">T</div>
            <span className="text-3xl font-black text-white self-center tracking-tighter">
                Todo<span className="text-gray-500">Pro</span>
            </span>
        </div>

        {/* 3D Card Effect */}
        <div className="bg-[#1e293b] p-10 rounded-[2.5rem] shadow-[0_20px_0_rgb(15,23,42),0_40px_60px_rgba(0,0,0,0.7)] border border-gray-800 transform hover:rotate-x-2 transition-transform duration-500 border-b-8 border-gray-900">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-black text-white tracking-tight">Welcome Back</h2>
            <p className="text-gray-400 mt-2 font-bold uppercase text-[10px] tracking-[0.2em]">Enter your secure workspace</p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="p-4 bg-red-500/10 text-red-400 text-xs rounded-2xl border border-red-500/20 font-black text-center uppercase tracking-widest">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-6 py-4 bg-[#0f172a] border-2 border-transparent focus:border-white rounded-2xl outline-none transition-all placeholder:text-gray-600 font-bold text-white shadow-inner"
                placeholder="name@company.com"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center ml-1">
                <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest leading-none">Password</label>
                <Link href="#" className="text-[10px] font-black text-gray-400 hover:text-white uppercase leading-none">Forgot?</Link>
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-6 py-4 bg-[#0f172a] border-2 border-transparent focus:border-white rounded-2xl outline-none transition-all placeholder:text-gray-600 font-bold text-white shadow-inner"
                placeholder="••••••••"
              />
            </div>

            {/* 3D Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-5 bg-white text-[#0f172a] rounded-2xl hover:bg-gray-100 transition-all flex items-center justify-center gap-3 font-black text-xs uppercase tracking-[0.2em] shadow-[0_6px_0_rgb(203,213,225),0_15px_30px_rgba(0,0,0,0.3)] active:shadow-none active:translate-y-1.5"
            >
              {loading ? "Verifying..." : (
                <>
                  Enter Workspace <ArrowRight size={18} strokeWidth={3} />
                </>
              )}
            </button>
          </form>

          <p className="mt-10 text-center text-gray-500 font-bold text-[10px] uppercase tracking-widest">
            Don&apos;t have an account?{" "}
            <Link href="/signup" className="text-white hover:underline underline-offset-4 font-black transition-all">
              Sign Up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
