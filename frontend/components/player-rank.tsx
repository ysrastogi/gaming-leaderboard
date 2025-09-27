"use client"

import type React from "react"

import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { AlertCircle, Loader2, Search, TrendingUp, User } from "lucide-react"
import { useState } from "react"

interface RankData {
  user_id: string
  username: string
  rank: number
  total_score: number
  total_sessions: number
}

interface RankState {
  data: RankData | null
  loading: boolean
  error: string | null
}

export default function PlayerRank() {
  const [userId, setUserId] = useState("")
  const [state, setState] = useState<RankState>({
    data: null,
    loading: false,
    error: null,
  })

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!userId.trim()) {
      setState((prev) => ({ ...prev, error: "User ID is required" }))
      return
    }

    setState({ data: null, loading: true, error: null })

    try {
      const response = await fetch(`/api/leaderboard/rank/${encodeURIComponent(userId.trim())}`)

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("Player not found. Make sure the user ID is correct.")
        }
        throw new Error(`Failed to fetch rank: ${response.statusText}`)
      }

      const data = await response.json()
      setState({
        data: data,
        loading: false,
        error: null,
      })
    } catch (error) {
      setState({
        data: null,
        loading: false,
        error: error instanceof Error ? error.message : "Failed to fetch player rank",
      })
    }
  }

  const getRankDisplay = (rank: number) => {
    if (rank === 1) return "1st Place 🏆"
    if (rank === 2) return "2nd Place 🥈"
    if (rank === 3) return "3rd Place 🥉"
    return `${rank}${getOrdinalSuffix(rank)} Place`
  }

  const getOrdinalSuffix = (num: number) => {
    const j = num % 10
    const k = num % 100
    if (j === 1 && k !== 11) return "st"
    if (j === 2 && k !== 12) return "nd"
    if (j === 3 && k !== 13) return "rd"
    return "th"
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSearch} className="space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 space-y-2">
            <Label htmlFor="searchUserId">User ID</Label>
            <Input
              id="searchUserId"
              type="text"
              placeholder="Enter user ID to check rank"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              disabled={state.loading}
            />
          </div>
          <div className="flex items-end">
            <Button type="submit" disabled={state.loading} className="w-full sm:w-auto">
              {state.loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Searching...
                </>
              ) : (
                <>
                  <Search className="mr-2 h-4 w-4" />
                  Check Rank
                </>
              )}
            </Button>
          </div>
        </div>
      </form>

      {state.error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{state.error}</AlertDescription>
        </Alert>
      )}

      {state.data && (
        <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-blue-200 dark:border-blue-800">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-blue-100 dark:bg-blue-900/50 rounded-full">
                  <User className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{state.data.username}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">Player Ranking</p>
                </div>
              </div>
              <div className="text-right">
                <div className="flex items-center space-x-2 mb-1">
                  <TrendingUp className="h-5 w-5 text-green-500" />
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">#{state.data.rank}</span>
                </div>
                <p className="text-sm font-medium text-blue-600 dark:text-blue-400">
                  {getRankDisplay(state.data.rank)}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Total Score: {state.data.total_score.toLocaleString()} | Total Sessions: {state.data.total_sessions}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
