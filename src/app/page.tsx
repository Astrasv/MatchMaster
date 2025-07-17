'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { TrophyIcon, UsersIcon, CalendarIcon, BarChartIcon } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { useAuthStore } from '@/lib/store';

const features = [
  {
    name: 'Tournament Management',
    description: 'Create and manage tournaments with the proven Pair Table Algorithm',
    icon: TrophyIcon,
  },
  {
    name: 'Team Organization',
    description: 'Organize teams with home ground assignments and detailed profiles',
    icon: UsersIcon,
  },
  {
    name: 'Smart Scheduling',
    description: 'Optimal match scheduling for fair rest days and reduced travel',
    icon: CalendarIcon,
  },
  {
    name: 'Real-time Analytics',
    description: 'Track performance with comprehensive statistics and insights',
    icon: BarChartIcon,
  },
];

export default function HomePage() {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-2">
            <TrophyIcon className="h-8 w-8 text-blue-500" />
            <span className="text-2xl font-bold text-white">MatchMaster</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/login">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="container text-center">
          <h1 className="text-5xl font-bold text-white mb-6">
            The Ultimate Tournament
            <span className="text-blue-500"> Management Platform</span>
          </h1>
          <p className="text-xl text-slate-300 mb-8 max-w-3xl mx-auto">
            Powered by the innovative Pair Table Algorithm, MatchMaster delivers optimal 
            tournament scheduling with fair rest days, home ground advantages, and minimal travel requirements.
          </p>
          <div className="flex items-center justify-center space-x-4">
            <Link href="/register">
              <Button size="lg">Start Your Tournament</Button>
            </Link>
            <Link href="/demo">
              <Button variant="secondary" size="lg">View Demo</Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-slate-800/50">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">
              Everything You Need for Tournament Success
            </h2>
            <p className="text-lg text-slate-300 max-w-2xl mx-auto">
              Built with proven algorithms and modern technology to deliver 
              the most comprehensive tournament management experience.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => (
              <Card key={feature.name} className="text-center">
                <CardHeader>
                  <feature.icon className="h-12 w-12 text-blue-500 mx-auto mb-4" />
                  <CardTitle className="text-lg">{feature.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{feature.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Algorithm Highlight */}
      <section className="py-20">
        <div className="container">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold text-white mb-6">
              Powered by the Pair Table Algorithm
            </h2>
            <p className="text-lg text-slate-300 mb-8">
              Our proprietary scheduling algorithm ensures optimal tournament organization 
              with balanced rest periods, strategic home ground allocation, and minimized 
              inter-country travel - delivering fairness and efficiency that traditional 
              Round Robin systems can't match.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-500 mb-2">Fair</div>
                <p className="text-slate-300">Balanced rest days for all teams</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-500 mb-2">Efficient</div>
                <p className="text-slate-300">Optimized travel and scheduling</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-500 mb-2">Strategic</div>
                <p className="text-slate-300">Home ground advantage distribution</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-700 bg-slate-900 py-12">
        <div className="container text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <TrophyIcon className="h-6 w-6 text-blue-500" />
            <span className="text-xl font-bold text-white">MatchMaster</span>
          </div>
          <p className="text-slate-400">
            © 2025 MatchMaster. Tournament management reimagined.
          </p>
        </div>
      </footer>
    </div>
  );
}