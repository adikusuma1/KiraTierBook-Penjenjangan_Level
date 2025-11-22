"use client";

import { useState } from "react";
import { Search, BookOpen, AlertCircle, CheckCircle2 } from "lucide-react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";

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
  screenshots: string[]; 
  analysis: AIAnalysis;  
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  
  const [result, setResult] = useState<BookResult | null>(null);
  const [error, setError] = useState("");

  const handleSearch = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {

      const apiUrl = "http://localhost:8000"; 
      const response = await axios.post(`${apiUrl}/api/analyze`, {
        title: query,
      });

      setResult(response.data);
      
    } catch (err: any) {
      console.error(err);
      setError(
        err.response?.data?.detail || "Gagal menganalisis buku. Pastikan Backend menyala."
      );
    } finally {
      setLoading(false);
    }
  };

  // Helper untuk warna badge berdasarkan respon AI
  const getBadgeColor = (color: string) => {
    const map: Record<string, string> = {
      MERAH: "bg-red-600 hover:bg-red-700",
      UNGU: "bg-purple-600 hover:bg-purple-700",
      BIRU: "bg-blue-600 hover:bg-blue-700",
      HIJAU: "bg-green-600 hover:bg-green-700",
      KUNING: "bg-yellow-500 hover:bg-yellow-600 text-black",
    };
    return map[color?.toUpperCase()] || "bg-gray-500";
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12 font-sans">
      <div className="mx-auto max-w-5xl">
        <div className="mb-10 text-center space-y-4">
          <h1 className="text-5xl font-extrabold text-slate-900 tracking-tight">
            AI Book <span className="text-blue-600">Classifier</span>
          </h1>
          <p className="text-xl text-slate-600">
            Klasifikasi Jenjang Buku Kemendikbud Menggunakan AI Vision
          </p>
        </div>

        {/* Search Bar */}
        <div className="mb-10 flex justify-center">
          <form onSubmit={handleSearch} className="relative w-full max-w-2xl flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <Input
                type="text"
                placeholder="Masukkan judul buku (Contoh: Laskar Pelangi)..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="pl-12 h-14 text-lg rounded-xl shadow-sm"
              />
            </div>
            <Button 
              type="submit" 
              disabled={loading} 
              className="h-14 px-8 text-lg rounded-xl bg-blue-600 hover:bg-blue-700"
            >
              {loading ? "Memproses..." : "Analisis"}
            </Button>
          </form>
        </div>

        {/* Error Alert */}
        {error && (
          <Alert className="mb-6 bg-red-50 border-red-200 text-red-700">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Loading Skeleton */}
        {loading && (
          <Card className="rounded-3xl border-slate-200 shadow-sm">
            <CardContent className="p-8 flex gap-8">
              <Skeleton className="w-1/3 h-64 rounded-xl" />
              <div className="w-2/3 space-y-4">
                <Skeleton className="h-8 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
                <div className="space-y-2 mt-8">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* --- 3. MENAMPILKAN HASIL (RESULT) --- */}
        {!loading && result && (
          <Card className="rounded-3xl border-slate-200 shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-300">
            <div className="flex flex-col md:flex-row">
              
              {/* Kolom Kiri: Bukti Screenshot */}
              <div className="w-full md:w-1/3 bg-slate-100 p-6 border-r border-slate-200 flex items-center justify-center">
                {result.screenshots && result.screenshots.length > 0 ? (
                  <div className="relative rounded-lg overflow-hidden shadow-md border border-slate-300">
                    <img 
                      src={`data:image/png;base64,${result.screenshots[0]}`} 
                      alt="Preview Buku" 
                      className="w-full h-auto object-contain"
                    />
                    <div className="absolute bottom-0 w-full bg-black/60 text-white text-xs text-center py-1">
                      AI Vision Evidence
                    </div>
                  </div>
                ) : (
                  <div className="text-slate-400 text-sm">No Preview Available</div>
                )}
              </div>

              {/* Kolom Kanan: Analisis */}
              <div className="w-full md:w-2/3 p-8 space-y-6">
                <div>
                  <div className="flex justify-between items-start">
                    <div>
                      <h2 className="text-3xl font-bold text-slate-900">{result.title}</h2>
                      <p className="text-slate-500 text-lg mt-1">
                        {result.authors?.join(", ")} • {result.page_count || "?"} Halaman
                      </p>
                    </div>
                    {/* Badge Jenjang */}
                    <Badge className={`px-4 py-2 text-md font-bold rounded-lg ${getBadgeColor(result.analysis.badge_color)}`}>
                      {result.analysis.jenjang}
                    </Badge>
                  </div>
                </div>

                <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100 space-y-4">
                  <div className="flex gap-3">
                    <CheckCircle2 className="h-6 w-6 text-blue-600 flex-shrink-0" />
                    <div>
                      <h3 className="font-semibold text-slate-900">Alasan Klasifikasi</h3>
                      <p className="text-slate-700 leading-relaxed mt-1">
                        {result.analysis.alasan}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3">
                    <BookOpen className="h-6 w-6 text-green-600 flex-shrink-0" />
                    <div>
                      <h3 className="font-semibold text-slate-900">Saran Pendampingan</h3>
                      <p className="text-slate-700 leading-relaxed mt-1">
                        {result.analysis.saran}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="text-right text-sm text-slate-400 font-medium">
                  AI Confidence Score: {result.analysis.confidence_score}%
                </div>
              </div>

            </div>
          </Card>
        )}

      </div>
    </div>
  );
}