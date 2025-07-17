'use client';

import Link from 'next/link';
import { CalendarIcon, UsersIcon, TrophyIcon } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { formatDate } from '@/lib/utils';

interface Tournament {
  id: string;
  name: string;
  description?: string;
  status: string;
  created_at: string;
  start_date?: string;
  end_date?: string;
}

interface TournamentCardProps {
  tournament: Tournament;
}

export function TournamentCard({ tournament }: TournamentCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-400 bg-green-400/10';
      case 'completed':
        return 'text-blue-400 bg-blue-400/10';
      case 'draft':
        return 'text-yellow-400 bg-yellow-400/10';
      default:
        return 'text-slate-400 bg-slate-400/10';
    }
  };

  return (
    <Card className="hover:bg-slate-700/50 transition-colors">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-lg">{tournament.name}</CardTitle>
            <CardDescription className="mt-1">
              {tournament.description || 'No description provided'}
            </CardDescription>
          </div>
          <span
            className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(
              tournament.status
            )}`}
          >
            {tournament.status.charAt(0).toUpperCase() + tournament.status.slice(1)}
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex items-center space-x-4 text-sm text-slate-400 mb-4">
          <div className="flex items-center">
            <CalendarIcon className="h-4 w-4 mr-1" />
            Created {formatDate(tournament.created_at)}
          </div>
          {tournament.start_date && (
            <div className="flex items-center">
              <TrophyIcon className="h-4 w-4 mr-1" />
              Starts {formatDate(tournament.start_date)}
            </div>
          )}
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 text-sm text-slate-400">
            <div className="flex items-center">
              <UsersIcon className="h-4 w-4 mr-1" />
              0 Teams
            </div>
          </div>
          <Link href={`/tournaments/${tournament.id}`}>
            <Button size="sm">View Details</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}