"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Loader2, RefreshCw, Trophy, Medal, Award, AlertCircle } from "lucide-react"

const API_URL= "http://localhost:8000"

interface Player {
  user_id: string
  username: string
  total_score?: number
  rank?: number
}

interface LeaderboardState {
  players: Player[]
  loading: boolean
  error: string | null
}

export default function Leaderboard() {
  const [state, setState] = useState<LeaderboardState>({
    players: [],
    loading: false,
    error: null,
  })

  const fetchLeaderboard = async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }))

    try {
      const response = await fetch(`${API_URL}/api/leaderboard/top`)

      if (!response.ok) {
        throw new Error(`Failed to fetch leaderboard: ${response.statusText}`)
      }

      const data = await response.json()

      const playersFormatted = data.map((player: any) => ({
        user_id: player.user_id,
        username: player.username,
        rank: player.rank,
        total_score: player.total_score
      }))

      setState({
        players: playersFormatted,
        loading: false,
        error: null,
      })

    } catch (error) {
      setState({
        players: [],
        loading: false,
        error: error instanceof Error ? error.message : "Failed to fetch leaderboard",
      })
    }
  }

  useEffect(() => {
    fetchLeaderboard()
  }, [])

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Trophy className="h-5 w-5 text-yellow-500" />
      case 2:
        return <Medal className="h-5 w-5 text-gray-400" />
      case 3:
        return <Award className="h-5 w-5 text-amber-600" />
      default:
        return <span className="text-lg font-bold text-gray-500">#{rank}</span>
    }
  }

  const getRankBadge = (rank: number) => {
    switch (rank) {
      case 1:
        return <Badge className="bg-yellow-500 hover:bg-yellow-600">1st</Badge>
      case 2:
        return <Badge className="bg-gray-400 hover:bg-gray-500">2nd</Badge>
      case 3:
        return <Badge className="bg-amber-600 hover:bg-amber-700">3rd</Badge>
      default:
        return <Badge variant="outline">#{rank}</Badge>
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Top 10 Players</h3>
        <Button onClick={fetchLeaderboard} disabled={state.loading} variant="outline" size="sm">
          {state.loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <RefreshCw className="mr-2 h-4 w-4" />}
          Refresh
        </Button>
      </div>

      {state.error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{state.error}</AlertDescription>
        </Alert>
      )}

      {state.loading && state.players.length === 0 ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-8 w-8 animate-spin text-gray-500" />
          <span className="ml-2 text-gray-500">Loading leaderboard...</span>
        </div>
      ) : (
        <div className="space-y-3">
          {state.players.length === 0 && !state.loading ? (
            <div className="text-center py-8 text-gray-500">No players found. Be the first to submit a score!</div>
          ) : (
            <>
              {/* Desktop Table View */}
              <div className="hidden md:block">
                <div className="overflow-hidden rounded-lg border">
                  <table className="w-full">
                    <thead className="bg-gray-50 dark:bg-gray-800">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Rank
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Player
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Score
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                      {state.players.map((player) => (
                        <tr key={player.username || player.user_id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">{getRankIcon(player.rank!)}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900 dark:text-white">{player.username || player.user_id}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-bold text-gray-900 dark:text-white">
                              {player.total_score.toLocaleString()}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Mobile Card View */}
              <div className="md:hidden space-y-3">
                {state.players.map((player) => (
                  <div
                    key={player.user_id}
                    className="bg-white dark:bg-gray-800 rounded-lg border p-4 flex items-center justify-between"
                  >
                    <div className="flex items-center space-x-3">
                      {getRankIcon(player.rank!)}
                      <div>
                        <div className="font-medium text-gray-900 dark:text-white">{player.user_id}</div>
                        <div className="text-sm text-gray-500">{getRankBadge(player.rank!)}</div>
                      </div>
                    </div>
                    <div className="text-lg font-bold text-gray-900 dark:text-white">
                      {player.total_score.toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}
