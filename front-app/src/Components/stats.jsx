/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stats.jsx                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/12/26 09:43:06 by jmykkane          #+#    #+#             */
/*   Updated: 2023/12/27 11:21:33 by jmykkane         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

import { useState, useEffect, useRef } from "react"
import axios from 'axios'
import gsap from 'gsap'

const Stats = () => {
  const [status, setStatus] = useState(false)
  const [hashrate, setHashrate] = useState(0)
  const [oldrate , setOldRate] = useState(0)
  const [power, setPower] = useState(0)
  const [rpm, setRpm] = useState(0)

  const hashRateRef = useRef(null)


  // Animating hashrate variable
  useEffect(() => {
    let newColor = '#FFFFFF'

    if (oldrate < hashrate) {
      newColor = '#90EE90'
    } else if (oldrate > hashrate) {
      newColor = '#F08080'
    }

    const tl = gsap.timeline()
    tl.to(hashRateRef.current, { color: newColor, duration: 0.4})
      .to(hashRateRef.current, { color: '#FFFFFF', duration: 0.75})
    
  }, [hashrate])

  useEffect(() => {
    const fetchStats = async () => {
      try {
        console.log('fetching stats')
        const response = await axios.get('/data/stats')
        const data = response.data

        setOldRate(hashrate)
        setHashrate(data.hashrate)
        setStatus(data.status)
        setPower(JSON.parse(data.power)[0].Rig_0)
        setRpm(data.fan)
      } catch(error) {
        console.log('Error on fetchStats: ', error)
      }
    }
    
    fetchStats()
    const interval = setInterval(fetchStats, 10000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="stats">
      {status ?
        <div className="grid-header"><h1>Miners <span className="stats-online">ON</span></h1></div>
      : 
        <div className="grid-header"><h1>Miners: <span className="stats-offline">OFF</span></h1></div>
      }
      
      <div className="info-item">
        <h2>MINING RATE</h2>
        <p><span ref={hashRateRef}>{hashrate}</span> MH/s</p>
      </div>

      <div className="info-item">
        <h2>POWER USAGE</h2>
        <p>{power} kW</p>
      </div>

      <div className="info-item">
        <h2>FAN SPEED</h2>
        <p>{rpm} rpm</p>
      </div>
      
     
      
    </div>
  )
}

export default Stats