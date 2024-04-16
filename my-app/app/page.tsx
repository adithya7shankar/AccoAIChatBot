import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar } from "@/components/ui/avatar"


export default function main() {

  const chats = [
    {
      message: "Hi there! foo bar biz!",
      sender: "Support Bot",
      time: "9:00am"
    },
    {
      message: "I'm having trouble with my order. Can you help me?",
      sender: "You",
      time: "9:05am"
    },
    // Add more chat messages as needed
  ];

  const sessions = [
    {
      id: 1,
      userid: 1,
      date: "2022-01-01"
    },
    {
      id: 2,
      userid: 1,
      date: "2022-01-01"
    },
    {
      id: 3,
      userid: 1,
      date: "2022-01-01"
    },
  ]

  return (
    <div key="1" className="flex flex-col min-h-screen">
      <header className="flex items-center h-14 border-b px-4">
        <div className="flex-1 font-semibold">Sessions</div>
        <Button className="ml-auto" size="sm" variant="outline">
          New Session
        </Button>
        <Button size="sm" variant="outline">
          New User
        </Button>
      </header>
      <div className="flex flex-1">
        <div className="w-[300px] border-r">
          <div className="flex items-center h-14 px-4 border-b">
            <SearchIcon className="mr-2 h-4 w-4 opacity-50" />
            <Input className="min-w-0" placeholder="Search sessions..." />
          </div>
          <div className="flex-1 overflow-auto">
            <nav className="px-2">
              {
                sessions.map((session, index) => (

                  <Button className="w-full text-left" variant="ghost">
                    <div className="flex items-center gap-2">
                      <MessageSquareIcon className="w-4 h-4" />
                    </div>
                    <p className="text-sm truncate w-[250px] last:mb-0">
                      session_{session.id}
                    </p>
                    <time className="text-sm ml-auto block">{session.date}</time>
                  </Button>
                ))
              }
            </nav>
          </div>
        </div>
        <div className="flex-1 flex flex-col">
          <div className="flex-1 p-4 bg-gray-100/40 dark:bg-gray-800/40">
            <div className="grid gap-4">

              {chats.map((chat, index) => (

                <div key={index} className="flex items-start gap-4">
                  <Avatar className="shrink-0" />
                  <div className="grid gap-1">
                    <div className="bg-white border border-gray-200 rounded-lg py-4 px-4 text-sm dark:bg-gray-900 dark:border-gray-800">
                      {chat.message}
                    </div>
                    <time className="text-xs text-gray-500 dark:text-gray-400">{chat.sender}</time>
                  </div>
                </div>

              ))}


            </div>
            <div className="mt-4 bg-gray-100/60 dark:bg-gray-800/60 p-4 rounded-lg">
              <input className="w-full p-2 rounded-md border" placeholder="Type your message here." type="text" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function MessageSquareIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  )
}


function SearchIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  )
}
