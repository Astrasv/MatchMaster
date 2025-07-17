'use client';

import { useEffect, useState } from 'react';
import { PlusIcon, SearchIcon, FilterIcon } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent } from '@/components/ui/Card';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { TournamentCard } from '@/components/tournaments/TournamentCard';
import { useTournamentStore } from '@/lib/store';
import { tournamentAPI } from '@/lib/api';

export default function TournamentsPage() {
  const { tournaments, setTournaments } = useTournamentStore();
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

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

  const filteredTournaments = tournaments.filter((tournament) => {
    const matchesSearch = tournament.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         tournament.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || tournament.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="flex h-screen bg-slate-900">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            {/* Page Header */}
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">Tournaments</h1>
                <p className="text-slate-400">
                  Manage all your tournaments powered by the Pair Table Algorithm
                </p>
              </div>
              <Button>
                <PlusIcon className="h-4 w-4 mr-2" />
                Create Tournament
              </Button>
            </div>

            {/* Filters */}
            <div className="flex items-center space-x-4 mb-6">
              <div className="relative flex-1 max-w-md">
                <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  type="search"
                  placeholder="Search tournaments..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="flex h-10 rounded-md border border-slate-600 bg-slate-800 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Status</option>
                <option value="draft">Draft</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
              </select>
              <Button variant="secondary" size="sm">
                <FilterIcon className="h-4 w-4 mr-2" />
                More Filters
              </Button>
            </div>

            {/* Tournament Grid */}
            {isLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <Card key={i} className="animate-pulse">
                    <CardContent className="p-6">
                      <div className="h-4 bg-slate-700 rounded w-3/4 mb-4"></div>
                      <div className="h-3 bg-slate-700 rounded w-full mb-2"></div>
                      <div className="h-3 bg-slate-700 rounded w-2/3 mb-4"></div>
                      <div className="flex justify-between items-center">
                        <div className="h-3 bg-slate-700 rounded w-1/3"></div>
                        <div className="h-8 bg-slate-700 rounded w-20"></div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : filteredTournaments.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredTournaments.map((tournament) => (
                  <TournamentCard key={tournament.id} tournament={tournament} />
                ))}
              </div>
            ) : (
              <Card>
                <CardContent className="text-center py-12">
                  <div className="text-slate-600 text-6xl mb-4">🏆</div>
                  <h3 className="text-lg font-medium text-white mb-2">
                    {searchTerm || statusFilter !== 'all' 
                      ? 'No tournaments found' 
                      : 'No tournaments yet'
                    }
                  </h3>
                  <p className="text-slate-400 mb-4">
                    {searchTerm || statusFilter !== 'all'
                      ? 'Try adjusting your search or filters'
                      : 'Create your first tournament to get started'
                    }
                  </p>
                  {(!searchTerm && statusFilter === 'all') && (
                    <Button>
                      <PlusIcon className="h-4 w-4 mr-2" />
                      Create Tournament
                    </Button>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}