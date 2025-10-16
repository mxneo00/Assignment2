import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  // Login States
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  // Hold HTML content from FastAPI
  const [htmlContent, setHtmlContent] = useState(null)
  const [redisContent, setRedisContent] = useState(null)

  const fastapiSetup = async () => {
    console.log("We are trying to reach out to FastAPI")
    try {
      const response = await axios.get("http://localhost:8000/react-demo")
      console.log(JSON.stringify(response.data));
      setHtmlContent(response.data)
    } catch (error) {
      console.error("Error fetching data: ", error);
      setHtmlContent("<p style='color:red;'>Failed to fetch data.</p>");
    }
  }

  const redisTestSet = async () => {
    console.log("We are trying to reach out to Redis")
    try {
      const response = await axios.get("http://localhost:8000/redis-set-test")
      console.log(JSON.stringify(response.data));
      setRedisContent(response.data)
    } catch (error) {
      console.error("Error fetching data: ", error);
      setRedisContent("<p style='color:red;'>Failed to fetch data.</p>");
    }
  }

  const redisTestGet = async () => {
    console.log("We are trying to reach out to Redis")
    try {
      const response = await axios.get("http://localhost:8000/redis-get-test")
      console.log(JSON.stringify(response.data));
      setRedisContent(response.data)
    } catch (error) {
      console.error("Error fetching data: ", error);
      setRedisContent("<p style='color:red;'>Failed to fetch data.</p>");
    }
  }

  return (
    <>
      <Default />
    </>
  )
}

export default App
