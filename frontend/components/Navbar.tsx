"use client";

import { useState } from "react";
import Link from "next/link";
import { useModal } from "@/context/ModalContext";
import { useAuth } from "@/context/AuthContext";
import { useSearch } from "@/context/SearchContext";
import { useRouter, usePathname } from "next/navigation";
import {
  PlusCircle, LayoutDashboard, CheckCircle2, Search,
  Settings, LogOut, Menu, X, ListTodo, User, Clock, Filter
} from "lucide-react";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const { openTaskModal } = useModal();
  const { user, logout } = useAuth();
  const { searchQuery, setSearchQuery, activeFilter, setActiveFilter } = useSearch();
  const router = useRouter();
  const pathname = usePathname();

  const handleNavClick = (filter: "all" | "completed" | "pending") => {
    setActiveFilter(filter);
    if (pathname !== "/tasks") {
      router.push("/tasks");
    }
  };

  const handleSearchFocus = () => {
    if (pathname !== "/tasks") {
      router.push("/tasks");
    }
    setIsSearchOpen(true);
  };

  // Helper for active link styles - Shaded Glass Theme
  const linkClass = "flex items-center gap-2 px-4 py-2 rounded-xl transition-all duration-300 font-bold text-[11px] uppercase tracking-wider cursor-pointer whitespace-nowrap";
  const getActiveClass = (filter: string) => activeFilter === filter ? "bg-white text-[#0f172a] shadow-lg shadow-white/10" : "text-gray-400 hover:bg-white/5 hover:text-white";

  return (
    <nav className="sticky top-0 z-50 glass-panel border-b border-white/5 sm:mx-4 sm:mt-4 rounded-b-2xl sm:rounded-2xl shadow-2xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex justify-between h-20 items-center gap-4">
          {/* Logo Section */}
          <div className="flex items-center gap-3 shrink-0">
            <Link href="/tasks" className="flex items-center gap-2 group">
              <div className="relative">
                <div className="absolute -inset-1 bg-white rounded-xl blur opacity-10 group-hover:opacity-30 transition-all"></div>
                <div className="relative w-8 h-8 sm:w-10 sm:h-10 bg-white rounded-xl flex items-center justify-center text-[#0f172a] font-black text-sm sm:text-base">
                  T
                </div>
              </div>
              <span className="hidden sm:block text-xl font-black text-white tracking-tight">
                Todo<span className="text-gray-500 font-medium">Pro</span>
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-1 flex-1 justify-center">
            <button onClick={() => handleNavClick("all")} className={`${linkClass} ${getActiveClass("all")}`}>
              <LayoutDashboard size={14} /> Home
            </button>
            <button onClick={() => handleNavClick("all")} className={`${linkClass} ${getActiveClass("tasks")}`}>
              <ListTodo size={14} /> My Tasks
            </button>

            <div className="h-6 w-[1px] bg-white/10 mx-3"></div>

            <button onClick={() => handleNavClick("completed")} className={`${linkClass} ${getActiveClass("completed")}`}>
              <CheckCircle2 size={14} /> Completed
            </button>
            <button onClick={() => handleNavClick("pending")} className={`${linkClass} ${getActiveClass("pending")}`}>
              <Clock size={14} /> Pending
            </button>

            <div className="h-6 w-[1px] bg-white/10 mx-3"></div>

            <div className={`relative flex items-center transition-all duration-500 ${isSearchOpen ? 'w-64' : 'w-10 overflow-hidden'}`}>
                <Search size={14} className="absolute left-3 text-gray-500 pointer-events-none" />
                <input
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onFocus={handleSearchFocus}
                  onBlur={() => !searchQuery && setIsSearchOpen(false)}
                  placeholder="SEARCH DIRECTIVES..."
                  className={`bg-white/5 border border-white/10 rounded-xl py-2 pl-10 pr-4 text-white text-[10px] font-bold outline-none focus:border-white/20 w-full transition-all ${isSearchOpen ? 'opacity-100' : 'opacity-0'}`}
                />
                {!isSearchOpen && (
                  <button onClick={() => setIsSearchOpen(true)} className="absolute inset-0 flex items-center justify-center text-gray-400 hover:text-white">
                    <Search size={14} />
                  </button>
                )}
            </div>
          </div>

          {/* User Profile */}
          <div className="flex items-center gap-2 sm:gap-4 shrink-0">
            {user ? (
              <div className="flex items-center gap-2 sm:gap-4 pl-2 sm:pl-6 border-l border-white/5">
                <div className="hidden sm:flex flex-col items-end mr-1">
                  <span className="text-[10px] font-bold text-white leading-none tracking-tight">{user.name.split(' ')[0]}</span>
                  <span className="text-[8px] font-bold text-indigo-400 uppercase tracking-widest mt-1">Online</span>
                </div>
                <button className="w-8 h-8 sm:w-10 sm:h-10 rounded-full glass-input border border-white/10 flex items-center justify-center text-white hover:border-white/20 transition-all shadow-inner">
                  <User size={16} />
                </button>
                <button
                  onClick={logout}
                  className="p-2 sm:p-2.5 bg-white/5 text-gray-400 hover:bg-red-500/10 hover:text-red-400 rounded-xl transition-all border border-white/5"
                >
                  <LogOut size={16} />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-4 pl-6">
                 <Link href="/signin" className="text-gray-400 hover:text-white font-bold text-[11px] uppercase tracking-wider transition-colors">Sign In</Link>
                 <Link href="/signup" className="px-5 py-2.5 bg-white text-[#0f172a] rounded-xl hover:bg-gray-100 transition-all font-bold text-[11px] uppercase tracking-wider">Sign Up</Link>
              </div>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="lg:hidden p-2 sm:p-2.5 bg-white/5 text-white hover:bg-white/10 rounded-xl transition-all border border-white/5"
            >
              {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {isMenuOpen && (
        <div className="lg:hidden glass-panel border-t border-white/5 p-6 space-y-4 animate-in slide-in-from-top duration-300 rounded-b-2xl shadow-2xl">
          {/* Mobile Search Overlay */}
          <div className="relative">
              <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => pathname !== "/tasks" && router.push("/tasks")}
                placeholder="SEARCH FOR TASKS..."
                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-white text-xs font-bold outline-none"
              />
          </div>

          <div className="grid grid-cols-2 gap-3">
             <button onClick={() => { handleNavClick("all"); setIsMenuOpen(false); }} className="p-4 glass-input rounded-2xl font-bold text-[10px] uppercase tracking-widest text-white flex flex-col items-center gap-3 border border-white/5">
                <LayoutDashboard size={20} className="text-indigo-400" /> Home
             </button>
             <button onClick={() => { handleNavClick("all"); setIsMenuOpen(false); }} className="p-4 glass-input rounded-2xl font-bold text-[10px] uppercase tracking-widest text-white flex flex-col items-center gap-3 border border-white/5">
                <ListTodo size={20} className="text-indigo-400" /> Tasks
             </button>
             <button onClick={() => { handleNavClick("completed"); setIsMenuOpen(false); }} className="p-4 glass-input rounded-2xl font-bold text-[10px] uppercase tracking-widest text-white flex flex-col items-center gap-3 border border-white/5">
                <CheckCircle2 size={20} className="text-indigo-400" /> Done
             </button>
             <button onClick={() => { handleNavClick("pending"); setIsMenuOpen(false); }} className="p-4 glass-input rounded-2xl font-bold text-[10px] uppercase tracking-widest text-white flex flex-col items-center gap-3 border border-white/5">
                <Clock size={20} className="text-indigo-400" /> Active
             </button>
          </div>

          <button
              onClick={() => { openTaskModal(); setIsMenuOpen(false); }}
              className="w-full p-4 bg-indigo-500 text-white rounded-2xl font-bold text-[10px] uppercase tracking-[0.3em] flex items-center justify-center gap-3 shadow-xl active:scale-95 transition-all"
          >
              <PlusCircle size={20} /> Add New Directive
          </button>

          {user && (
            <button
                onClick={() => { logout(); setIsMenuOpen(false); }}
                className="w-full p-4 bg-white/5 text-red-400 font-bold text-[10px] uppercase tracking-widest rounded-2xl border border-red-500/10 flex items-center justify-center gap-3"
            >
                <LogOut size={18} /> Terminate Session
            </button>
          )}
        </div>
      )}
    </nav>
  );
}
