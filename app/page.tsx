import dynamic from 'next/dynamic'
import Header from './components/Header'
import BookingDialog from './components/BookingDialog'
import Hero from './components/Hero'
import Stats from './components/Stats'
import Specials from './components/Specials'
import Menu from './components/Menu'
import About from './components/About'
import Visit from './components/Visit'
import Events from './components/Events'
import Contact from './components/Contact'
import Footer from './components/Footer'

// Dynamically import AOS to avoid SSR issues
const AOSInit = dynamic(() => import('./components/AOSInit'), { ssr: false })

export default function Home() {
  return (
    <>
      <AOSInit />
      <Header />
      <main>
        <Hero />
        <Stats />
        <Specials />
        <Menu />
        <About />
        <Visit />
        <Events />
        <Contact />
      </main>
      <Footer />
      <BookingDialog />
    </>
  )
}
