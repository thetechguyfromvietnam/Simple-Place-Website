import React, { useState, useEffect } from 'react'

const DebugInfo = () => {
  const [screenInfo, setScreenInfo] = useState({
    width: 0,
    height: 0,
    isMobile: false,
    isTablet: false,
    isDesktop: false
  })

  useEffect(() => {
    const updateScreenInfo = () => {
      const width = window.innerWidth
      const height = window.innerHeight
      setScreenInfo({
        width,
        height,
        isMobile: width < 640,
        isTablet: width >= 640 && width < 1024,
        isDesktop: width >= 1024
      })
    }

    updateScreenInfo()
    window.addEventListener('resize', updateScreenInfo)
    return () => window.removeEventListener('resize', updateScreenInfo)
  }, [])

  return (
    <div className="fixed bottom-4 right-4 bg-black/80 text-white p-3 rounded-lg text-xs z-50">
      <div>Width: {screenInfo.width}px</div>
      <div>Height: {screenInfo.height}px</div>
      <div>Mobile: {screenInfo.isMobile ? 'Yes' : 'No'}</div>
      <div>Tablet: {screenInfo.isTablet ? 'Yes' : 'No'}</div>
      <div>Desktop: {screenInfo.isDesktop ? 'Yes' : 'No'}</div>
    </div>
  )
}

export default DebugInfo
