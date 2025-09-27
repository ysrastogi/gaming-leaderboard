"use client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Trophy, Target, Medal } from "lucide-react"
import ScoreSubmission from "@/components/score-submission"
import Leaderboard from "@/components/leaderboard"
import PlayerRank from "@/components/player-rank"

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Trophy className="h-8 w-8 text-yellow-500" />
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white">Gaming Leaderboard</h1>
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Submit your scores, check rankings, and compete with other players
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          <Tabs defaultValue="submit" className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-8">
              <TabsTrigger value="submit" className="flex items-center gap-2">
                <Target className="h-4 w-4" />
                Submit Score
              </TabsTrigger>
              <TabsTrigger value="leaderboard" className="flex items-center gap-2">
                <Trophy className="h-4 w-4" />
                Leaderboard
              </TabsTrigger>
              <TabsTrigger value="rank" className="flex items-center gap-2">
                <Medal className="h-4 w-4" />
                Check Rank
              </TabsTrigger>
            </TabsList>

            <TabsContent value="submit">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5" />
                    Submit Your Score
                  </CardTitle>
                  <CardDescription>Enter your user ID and score to submit to the leaderboard</CardDescription>
                </CardHeader>
                <CardContent>
                  <ScoreSubmission />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="leaderboard">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Trophy className="h-5 w-5" />
                    Top 10 Players
                  </CardTitle>
                  <CardDescription>See the highest scoring players on the leaderboard</CardDescription>
                </CardHeader>
                <CardContent>
                  <Leaderboard />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="rank">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Medal className="h-5 w-5" />
                    Check Player Rank
                  </CardTitle>
                  <CardDescription>Enter a user ID to see their current ranking</CardDescription>
                </CardHeader>
                <CardContent>
                  <PlayerRank />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
