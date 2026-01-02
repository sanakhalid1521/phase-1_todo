"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { UserPlus, Mail, Lock, ArrowRight, Github } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

export default function SignupPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    // Set user and redirect
    setTimeout(() => {
      login(name || email.split('@')[0], email);
      router.push("/tasks");
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 font-sans perspective-1000">
      <div className="max-w-md w-full animate-in zoom-in-95 duration-700">
        {/* Logo */}
        <div className="flex justify-center mb-10 gap-3">
            <div className="w-12 h-12 bg-white rounded-[1.2rem] flex items-center justify-center text-[#0f172a] font-black shadow-[0_0_30px_rgba(255,255,255,0.4)] transform -rotate-3">T</div>
            <span className="text-3xl font-black text-white self-center tracking-tighter">
                Todo<span className="text-gray-400 font-medium">Pro</span>
            </span>
        </div>

        {/* Glass 3D Card */}
        <div className="glass-card p-10 rounded-[3rem] shadow-[0_40px_80px_rgba(0,0,0,0.5)] transform hover:rotate-x-2 transition-all duration-500 relative overflow-hidden group">
          {/* Decorative Glow */}
          <div className="absolute -top-24 -right-24 w-48 h-48 bg-white/5 rounded-full blur-3xl group-hover:bg-white/10 transition-all duration-700"></div>

          <div className="text-center mb-10 relative z-10">
            <h2 className="text-4xl font-black text-white tracking-tight leading-none">Assemble</h2>
            <p className="text-gray-300 mt-3 font-black uppercase text-[10px] tracking-[0.4em] opacity-60 italic">Strategic Deployment Initiated</p>
          </div>

          <form className="space-y-6 relative z-10" onSubmit={handleSubmit}>
            {error && (
              <div className="p-4 bg-red-500/20 backdrop-blur-md text-red-200 text-xs rounded-2xl border border-red-500/30 font-black text-center uppercase tracking-widest">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Objective Lead</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-6 py-5 bg-white/5 border border-white/10 focus:border-white rounded-[1.5rem] outline-none transition-all placeholder:text-gray-600 font-bold text-white shadow-inner focus:bg-white/10"
                placeholder="Agent Name"
              />
            </div>

            <div className="space-y-2">
              <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Comm Channel</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-6 py-5 bg-white/5 border border-white/10 focus:border-white rounded-[1.5rem] outline-none transition-all placeholder:text-gray-600 font-bold text-white shadow-inner focus:bg-white/10"
                placeholder="secure@comms.org"
              />
            </div>

            <div className="space-y-2">
              <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Access Key</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-6 py-5 bg-white/5 border border-white/10 focus:border-white rounded-[1.5rem] outline-none transition-all placeholder:text-gray-600 font-bold text-white shadow-inner focus:bg-white/10"
                placeholder="••••••••"
              />
            </div>

            {/* Glass 3D Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-6 bg-white text-[#0f172a] rounded-[1.5rem] hover:bg-gray-100 transition-all flex items-center justify-center gap-4 font-black text-xs uppercase tracking-[0.4em] shadow-[0_0_40px_rgba(255,255,255,0.2)] active:scale-[0.98]"
            >
              {loading ? "AUTHENTICATING..." : (
                <>
                  INITIALIZE <ArrowRight size={20} strokeWidth={4} />
                </>
              )}
            </button>
          </form>

          <p className="mt-10 text-center text-gray-400 font-bold text-[10px] uppercase tracking-[0.2em] relative z-10">
            Known Entity?{" "}
            <Link href="/signin" className="text-white hover:text-indigo-400 transition-colors font-black">
              SIGN IN
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
