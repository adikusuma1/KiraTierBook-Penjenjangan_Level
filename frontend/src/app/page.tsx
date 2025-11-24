"use client";

import { useState } from "react";
import { Search, BookOpen, AlertCircle, CheckCircle2, Info, Book } from "lucide-react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";

// --- TIPE DATA ---
interface AIAnalysis {
  jenjang: string;
  confidence_score: number;
  alasan: string;
  saran: string;
  badge_color: string;
}

interface BookResult {
  title: string;
  authors: string[];
  page_count: number;
  categories: string[];
  thumbnail: string | null;
  screenshots: string[];
  analysis: AIAnalysis;
}

// --- KOMPONEN SIMBOL JENJANG ---
const LevelSymbol = ({ jenjang, colorCode }: { jenjang: string, colorCode: string }) => {
  const rawCode = jenjang.split(" ")[1]?.substring(0, 1) || "A"; 
  const displayCode = jenjang.split(" ")[1] || "A"; 

  const colors: Record<string, string> = {
    MERAH: "#DC2626",   
    UNGU: "#9333EA",    
    BIRU: "#2563EB",    
    HIJAU: "#16A34A",   
    KUNING: "#EAB308",  
  };

  const hex = colors[colorCode?.toUpperCase()] || "#6B7280";
  const wrapperClass = "relative flex items-center justify-center w-16 h-16 drop-shadow-xl z-20 transition-transform hover:scale-110";

  switch (rawCode) {
    case "A": 
      return (
        <div className={wrapperClass}>
           <svg viewBox="0 0 24 24" fill={hex} className="w-full h-full stroke-white stroke-[1.5]">
             <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
           </svg>
           <span className="absolute text-white font-black text-2xl mt-1 drop-shadow-md">{displayCode}</span>
        </div>
      );
    case "B": 
    case "C": 
      return (
        <div className={wrapperClass}>
           <div className="w-full h-full rounded-full border-[3px] border-white flex items-center justify-center shadow-md" style={{ backgroundColor: hex }}>
              <span className="text-white font-black text-2xl drop-shadow-md">{displayCode}</span>
           </div>
        </div>
      );
    case "D": 
      return (
        <div className={wrapperClass}>
           <svg viewBox="0 0 24 24" fill={hex} className="w-full h-full stroke-white stroke-[1.5] drop-shadow-sm">
             <path d="M12 2 L22 22 L2 22 Z" strokeLinejoin="round" />
           </svg>
           <span className="absolute text-white font-black text-xl mt-3 drop-shadow-md">{displayCode}</span>
        </div>
      );
    case "E": 
      return (
        <div className={wrapperClass}>
           <div className="w-14 h-14 border-[3px] border-white flex items-center justify-center shadow-md transform rotate-0" style={{ backgroundColor: hex }}>
              <span className="text-white font-black text-2xl drop-shadow-md">{displayCode}</span>
           </div>
        </div>
      );
    default: return null;
  }
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<BookResult | null>(null);
  const [error, setError] = useState("");
  // State tambahan untuk menangani gambar error
  const [imgError, setImgError] = useState(false);

  const handleSearch = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    setImgError(false); // Reset status error gambar setiap search baru

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await axios.post(`${apiUrl}/api/analyze`, { title: query });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Gagal menganalisis buku.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12 font-sans">
      <div className="mx-auto max-w-6xl">
        
        {/* Header & Search */}
        <div className="flex flex-col items-center mb-12 space-y-6">
          <h1 className="text-4xl md:text-5xl font-black text-slate-900 tracking-tight text-center">
            KiraTierBook <span className="text-blue-600">Penjenjangan Level</span>
          </h1>
          <p className="text-slate-500 text-lg max-w-2xl text-center">
            Klasifikasi Jenjang Buku Standar Kemdiktisaintek
          </p>
          
          <form onSubmit={handleSearch} className="w-full max-w-2xl flex gap-2 relative mt-4">
            <div className="relative flex-1 group">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5 group-focus-within:text-blue-500 transition-colors" />
              <Input
                type="text"
                placeholder="Masukkan judul buku (Contoh: Harry Potter)..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="pl-12 h-14 text-lg rounded-2xl border-slate-200 shadow-sm focus:ring-2 focus:ring-blue-500/20 transition-all bg-white"
              />
            </div>
            <Button type="submit" disabled={loading} className="h-14 px-8 rounded-2xl text-lg font-semibold bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-600/20 transition-all">
              {loading ? "Memproses..." : "Analisis"}
            </Button>
          </form>
        </div>

        {/* Error */}
        {error && (
          <Alert className="max-w-2xl mx-auto mb-8 bg-red-50 border-red-100 text-red-700 rounded-2xl">
            <AlertCircle className="h-5 w-5" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Loading Skeleton */}
        {loading && (
          <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-8">
            <div className="md:col-span-4">
               <Skeleton className="w-full aspect-[2/3] rounded-3xl" />
            </div>
            <div className="md:col-span-8 space-y-6 pt-4">
               <Skeleton className="h-12 w-3/4 rounded-xl" />
               <Skeleton className="h-6 w-1/2 rounded-lg" />
               <div className="grid grid-cols-2 gap-4 mt-8">
                 <Skeleton className="h-32 w-full rounded-2xl" />
                 <Skeleton className="h-32 w-full rounded-2xl" />
               </div>
            </div>
          </div>
        )}

        {/* RESULT CARD */}
        {!loading && result && (
          <div className="max-w-5xl mx-auto bg-white rounded-[2.5rem] shadow-2xl border border-slate-100 overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-500">
            <div className="grid grid-cols-1 md:grid-cols-12">
              
              {/* --- KOLOM KIRI: VISUAL --- */}
              <div className="md:col-span-4 bg-slate-100 p-8 flex flex-col items-center justify-center relative overflow-hidden min-h-[400px]">
                <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#64748b_1px,transparent_1px)] [background-size:20px_20px]"></div>
                
                <div className="relative z-10 group">
                  <div className="absolute -inset-1 bg-black/20 blur-xl rounded-[14px] group-hover:blur-2xl transition-all duration-500"></div>
                  
                  <div className="relative rounded-[14px] overflow-hidden border-4 border-white shadow-2xl transition-transform duration-500 group-hover:-translate-y-2 w-[220px] bg-white">
                    {/* LOGIKA TAMPILAN GAMBAR: */}
                    {/* 1. Jika ada thumbnail dan belum error -> Tampilkan Cover Asli */}
                    {result.thumbnail && !imgError ? (
                      <img 
                        src={result.thumbnail} 
                        alt={result.title} 
                        className="w-full h-auto object-cover min-h-[300px]"
                        onError={() => setImgError(true)} // Jika gagal load, trigger error
                      />
                    ) : (
                      // 2. Jika tidak ada cover / error -> Tampilkan Karakter Lucu (Fallback)
                      <div className="w-full aspect-[2/3] bg-slate-50 flex flex-col items-center justify-center text-center p-4 relative overflow-hidden">
                        {/* Pastikan file no-cover.png ada di folder /public frontend */}
                        <img 
                          src="/no-cover.png" 
                          alt="Character" 
                          className="w-32 h-32 object-contain mb-2 drop-shadow-md animate-in bounce-in duration-700"
                        />
                        <span className="font-bold text-slate-400 text-sm uppercase tracking-widest mt-2">
                          Cover Not<br/>Available
                        </span>
                      </div>
                    )}
                  </div>

                  <div className="absolute -top-3 -right-3 z-30 filter drop-shadow-lg">
                    <LevelSymbol 
                      jenjang={result.analysis.jenjang} 
                      colorCode={result.analysis.badge_color} 
                    />
                  </div>
                </div>

                <div className="mt-8 flex items-center gap-2 text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  <CheckCircle2 className="w-4 h-4 text-green-500" />
                  AI Verified Content
                </div>
              </div>

              {/* --- KOLOM KANAN: DATA TEKS --- */}
              <div className="md:col-span-8 p-8 md:p-12 flex flex-col">
                <div className="mb-8">
                  <div className="flex flex-wrap gap-2 mb-3">
                    {result.categories?.map((cat, i) => (
                      <span key={i} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-bold uppercase tracking-wide">
                        {cat}
                      </span>
                    ))}
                  </div>
                  <h2 className="text-3xl md:text-4xl font-black text-slate-900 leading-tight mb-2">{result.title}</h2>
                  <p className="text-lg text-slate-500 font-medium">
                    Oleh <span className="text-slate-800">{result.authors?.join(", ")}</span> • {result.page_count} Halaman
                  </p>
                </div>

                <div className="grid grid-cols-1 gap-4 mb-8">
                  <div className="bg-blue-50/50 p-6 rounded-3xl border border-blue-100 hover:border-blue-200 transition-colors group">
                    <div className="flex gap-4">
                      <div className="bg-blue-600 w-10 h-10 rounded-xl flex items-center justify-center shrink-0 text-white shadow-lg shadow-blue-600/20 group-hover:scale-110 transition-transform">
                        <Info className="w-5 h-5" />
                      </div>
                      <div>
                        <h3 className="font-bold text-slate-900 text-lg">Analisis Teknis</h3>
                        <p className="text-slate-600 leading-relaxed mt-2 text-sm whitespace-pre-line">
                          {result.analysis.alasan}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-green-50/50 p-6 rounded-3xl border border-green-100 hover:border-green-200 transition-colors group">
                    <div className="flex gap-4">
                      <div className="bg-green-600 w-10 h-10 rounded-xl flex items-center justify-center shrink-0 text-white shadow-lg shadow-green-600/20 group-hover:scale-110 transition-transform">
                        <BookOpen className="w-5 h-5" />
                      </div>
                      <div>
                        <h3 className="font-bold text-slate-900 text-lg">Saran Pendampingan</h3>
                        <p className="text-slate-600 leading-relaxed mt-2 text-sm">
                          {result.analysis.saran}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-auto flex justify-between items-center pt-6 border-t border-slate-100">
                  <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Berdasarkan SK 030/P/2022
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Confidence</span>
                    <Badge variant="secondary" className="bg-slate-900 text-white px-3 py-1 rounded-lg">
                      {result.analysis.confidence_score}%
                    </Badge>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}