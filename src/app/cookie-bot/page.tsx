'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, Cookie, Search, Trash2 } from 'lucide-react';

interface CookieData {
  id: string;
  name: string;
  value: string;
  domain: string;
  path: string;
  secure: boolean;
  httpOnly: boolean;
  sameSite: string;
  expires?: string;
  size: number;
  timestamp: string;
}

export default function CookieBotPage() {
  const [keyword, setKeyword] = useState('');
  const [country, setCountry] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [cookies, setCookies] = useState<CookieData[]>([]);
  const [scanResults, setScanResults] = useState<Array<{metric: string; value: string | number}>>([]);
  const [progress, setProgress] = useState(0);

  const countries = [
    { code: 'TR', name: 'Türkiye' },
    { code: 'US', name: 'Amerika' },
    { code: 'GB', name: 'İngiltere' },
    { code: 'DE', name: 'Almanya' },
    { code: 'FR', name: 'Fransa' },
    { code: 'IT', name: 'İtalya' },
    { code: 'ES', name: 'İspanya' },
    { code: 'RU', name: 'Rusya' },
    { code: 'CN', name: 'Çin' },
    { code: 'JP', name: 'Japonya' },
    { code: 'BR', name: 'Brezilya' },
    { code: 'IN', name: 'Hindistan' },
  ];

  // Simulated cookie scanning function
  const scanForCookies = async () => {
    if (!keyword || !country) {
      alert('Lütfen kelime ve ülke seçiniz!');
      return;
    }

    setIsScanning(true);
    setProgress(0);
    setCookies([]);
    setScanResults([]);

    try {
      // Simulate progress
      for (let i = 0; i <= 100; i += 10) {
        setProgress(i);
        await new Promise(resolve => setTimeout(resolve, 200));
      }

      // Generate sample cookie data based on keyword and country
      const sampleCookies: CookieData[] = [
        {
          id: '1',
          name: `session_${keyword}_${country}`,
          value: `${Math.random().toString(36).substring(7)}`,
          domain: `.${keyword.toLowerCase()}.com`,
          path: '/',
          secure: true,
          httpOnly: true,
          sameSite: 'Lax',
          expires: new Date(Date.now() + 86400000).toISOString(),
          size: 48,
          timestamp: new Date().toISOString(),
        },
        {
          id: '2',
          name: `analytics_${keyword}`,
          value: `GA1.2.${Math.random().toString().substring(2, 12)}.${Math.random().toString().substring(2, 12)}`,
          domain: `.google-analytics.com`,
          path: '/',
          secure: true,
          httpOnly: false,
          sameSite: 'None',
          expires: new Date(Date.now() + 31536000000).toISOString(),
          size: 32,
          timestamp: new Date().toISOString(),
        },
        {
          id: '3',
          name: `pref_${country.toLowerCase()}`,
          value: `lang=${country.toLowerCase()}&theme=dark&${keyword}=enabled`,
          domain: `.example.com`,
          path: '/',
          secure: false,
          httpOnly: false,
          sameSite: 'Strict',
          size: 56,
          timestamp: new Date().toISOString(),
        },
        {
          id: '4',
          name: `tracking_${keyword}`,
          value: `usr_${Math.random().toString(36).substring(2, 15)}`,
          domain: `.ads.yahoo.com`,
          path: '/',
          secure: true,
          httpOnly: true,
          sameSite: 'None',
          expires: new Date(Date.now() + 7776000000).toISOString(),
          size: 28,
          timestamp: new Date().toISOString(),
        },
        {
          id: '5',
          name: `${keyword}_consent`,
          value: `accepted_${country}_${Date.now()}`,
          domain: `.${keyword.toLowerCase()}-site.org`,
          path: '/',
          secure: true,
          httpOnly: false,
          sameSite: 'Lax',
          expires: new Date(Date.now() + 15552000000).toISOString(),
          size: 42,
          timestamp: new Date().toISOString(),
        }
      ];

      setCookies(sampleCookies);
      
      // Generate scan results summary
      setScanResults([
        { metric: 'Toplam Çerez', value: sampleCookies.length },
        { metric: 'Güvenli Çerezler', value: sampleCookies.filter(c => c.secure).length },
        { metric: 'HttpOnly Çerezler', value: sampleCookies.filter(c => c.httpOnly).length },
        { metric: 'Kalıcı Çerezler', value: sampleCookies.filter(c => c.expires).length },
        { metric: 'Toplam Boyut', value: `${sampleCookies.reduce((sum, c) => sum + c.size, 0)} bytes` },
      ]);

    } catch (error) {
      console.error('Tarama hatası:', error);
      alert('Tarama sırasında bir hata oluştu!');
    } finally {
      setIsScanning(false);
      setProgress(100);
    }
  };

  const clearResults = () => {
    setCookies([]);
    setScanResults([]);
    setProgress(0);
  };

  const exportResults = () => {
    const data = {
      keyword,
      country,
      scanDate: new Date().toISOString(),
      cookies,
      summary: scanResults
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cookie-scan-${keyword}-${country}-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold mb-4 flex items-center justify-center gap-3">
          <Cookie className="w-10 h-10 text-orange-500" />
          Çerez Toplama Botu
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Girdiğiniz kelime ve ülkeye göre web sitelerindeki çerezleri hızlıca tarayın ve analiz edin.
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Kontrol Paneli */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Search className="w-5 h-5" />
                Tarama Ayarları
              </CardTitle>
              <CardDescription>
                Çerez taraması için parametreleri belirleyin
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="keyword">Anahtar Kelime</Label>
                <Input
                  id="keyword"
                  placeholder="Örn: shopping, news, social"
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)}
                  disabled={isScanning}
                />
              </div>
              
              <div>
                <Label htmlFor="country">Ülke</Label>
                <Select value={country} onValueChange={setCountry} disabled={isScanning}>
                  <SelectTrigger>
                    <SelectValue placeholder="Ülke seçiniz" />
                  </SelectTrigger>
                  <SelectContent>
                    {countries.map((c) => (
                      <SelectItem key={c.code} value={c.code}>
                        {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {isScanning && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Tarama İlerlemesi</span>
                    <span>{progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </div>
              )}

              <div className="flex gap-2">
                <Button 
                  onClick={scanForCookies} 
                  disabled={isScanning || !keyword || !country}
                  className="flex-1"
                >
                  {isScanning ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Taranıyor...
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4 mr-2" />
                      Taramayı Başlat
                    </>
                  )}
                </Button>
                
                {cookies.length > 0 && (
                  <Button 
                    variant="outline" 
                    onClick={clearResults}
                    disabled={isScanning}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                )}
              </div>

              {cookies.length > 0 && (
                <Button 
                  variant="secondary" 
                  onClick={exportResults}
                  className="w-full"
                  disabled={isScanning}
                >
                  Sonuçları Dışa Aktar
                </Button>
              )}
            </CardContent>
          </Card>

          {/* Özet İstatistikler */}
          {scanResults.length > 0 && (
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Tarama Özeti</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {scanResults.map((result, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">{result.metric}</span>
                      <Badge variant="secondary">{result.value}</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Çerez Listesi */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Cookie className="w-5 h-5" />
                Bulunan Çerezler
                {cookies.length > 0 && (
                  <Badge variant="outline">{cookies.length} adet</Badge>
                )}
              </CardTitle>
              <CardDescription>
                {keyword && country 
                  ? `"${keyword}" kelimesi ve ${countries.find(c => c.code === country)?.name} için tarama sonuçları`
                  : 'Çerez taraması başlatmak için parametreleri giriniz'
                }
              </CardDescription>
            </CardHeader>
            <CardContent>
              {cookies.length === 0 ? (
                <div className="text-center py-8">
                  <Cookie className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
                  <p className="text-muted-foreground">
                    Henüz çerez taraması yapılmadı. Taramayı başlatmak için sol paneli kullanın.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {cookies.map((cookie) => (
                    <Card key={cookie.id} className="border-l-4 border-l-blue-500">
                      <CardContent className="pt-4">
                        <div className="grid md:grid-cols-2 gap-4">
                          <div>
                            <h4 className="font-semibold text-lg mb-2">{cookie.name}</h4>
                            <div className="space-y-1 text-sm">
                              <div><strong>Domain:</strong> {cookie.domain}</div>
                              <div><strong>Path:</strong> {cookie.path}</div>
                              <div><strong>Boyut:</strong> {cookie.size} bytes</div>
                            </div>
                          </div>
                          <div>
                            <div className="mb-2">
                              <strong className="text-sm">Değer:</strong>
                              <code className="block mt-1 p-2 bg-muted rounded text-xs break-all">
                                {cookie.value}
                              </code>
                            </div>
                            <div className="flex flex-wrap gap-1">
                              {cookie.secure && <Badge variant="default">Güvenli</Badge>}
                              {cookie.httpOnly && <Badge variant="secondary">HttpOnly</Badge>}
                              <Badge variant="outline">SameSite: {cookie.sameSite}</Badge>
                            </div>
                            {cookie.expires && (
                              <div className="text-xs text-muted-foreground mt-2">
                                Sona erme: {new Date(cookie.expires).toLocaleString('tr-TR')}
                              </div>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}