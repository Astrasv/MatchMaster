'use client';

import { useEffect, useState } from 'react';
import { PlusIcon, TrophyIcon, UsersIcon, CalendarIcon, BarChartIcon } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { TournamentCard } from '@/components/tournaments/TournamentCard';
import { useAuthStore, useTournamentStore } from '@/lib/store';
import { tournamentAPI } from '@/lib/api';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { tournaments, setTournaments } = useTournamentStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchTournaments = async () => {
      try {
        const response = await tournamentAPI.getTournaments();
        setTournaments(response.data);
      } catch (error) {
        console.error('Failed to fetch tournaments:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTournaments();
  }, [setTournaments]);

  const stats = [
    {
      name: 'Active Tournaments',
      value: tournaments.filter(t => t.status === 'active').length,
      icon: TrophyIcon,
      color: 'text-blue-500',
    },
    {
      name: 'Total Teams',
      value: '0', // This would come from API
      icon: UsersIcon,
      color: 'text-green-500',
    },
    {
      name: 'Matches Played',
      value: '0', // This would come from API
      icon: CalendarIcon,
      color: 'text-purple-500',
    },
    {
      name: 'Completion Rate',
      value: '0%', // This would come from API
      icon: BarChartIcon,
      color: 'text-yellow-500',
    },
  ];

  return (
    <div className="flex h-screen bg-slate-900">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            {/* Welcome Section */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-white mb-2">
                Welcome back, {user?.username}!
              </h1>
              <p className="text-slate-400">
                Manage your tournaments with the power of the Pair Table Algorithm
              </p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {stats.map((stat) => (
                <Card key={stat.name}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-400">{stat.name}</p>
                        <p className="text-2xl font-bold text-white">{stat.value}</p>
                      </div>
                      <stat.icon className={`h-8 w-8 ${stat.color}`} />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Quick Actions */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-white">Quick Actions</h2>
              </div>
              <div className="flex space-x-4">
                <Button className="flex items-center">
                  <PlusIcon className="h-4 w-4 mr-2" />
                  Create Tournament
                </Button>
                <Button variant="secondary">
                  <UsersIcon className="h-4 w-4 mr-2" />
                  Add Teams
                </Button>
                <Button variant="secondary">
                  <CalendarIcon className="h-4 w-4 mr-2" />
                  Schedule Matches
                </Button>
              </div>
            </div>

            {/* Recent Tournaments */}
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-white">Recent Tournaments</h2>
                <Button variant="ghost" size="sm">
                  View All
                </Button>
              </div>
              
              {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {[...Array(3)].map((_, i) => (
                    <Card key={i} className="animate-pulse">
                      <CardHeader>
                        <div className="h-4 bg-slate-700 rounded w-3/4 mb-2"></div>
                        <div className="h-3 bg-slate-700 rounded w-1/2"></div>
                      </CardHeader>
                      <CardContent>
                        <div className="h-3 bg-slate-700 rounded w-full mb-2"></div>
                        <div className="h-3 bg-slate-700 rounded w-2/3"></div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              ) : tournaments.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {tournaments.slice(0, 6).map((tournament) => (
                    <TournamentCard key={tournament.id} tournament={tournament} />
                  ))}
                </div>
              ) : (
                <Card>
                  <CardContent className="text-center py-12">
                    <TrophyIcon className="h-12 w-12 text-slate-600 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-white mb-2">No tournaments yet</h3>
                    <p className="text-slate-400 mb-4">
                      Create your first tournament to get started with MatchMaster
                    </p>
                    <Button>
                      <PlusIcon className="h-4 w-4 mr-2" />
                      Create Tournament
                    </Button>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}