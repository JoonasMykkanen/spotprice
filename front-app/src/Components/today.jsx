/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   today.jsx                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/12/26 12:39:18 by jmykkane          #+#    #+#             */
/*   Updated: 2023/12/27 11:43:04 by jmykkane         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

import { useEffect, useState } from "react"
import axios from 'axios'

const Today = () => {
  const [revenue, setRevenue] = useState(0)
  const [profit, setProfit] = useState(0)
  const [cost, setCost] = useState(0)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/data/today')
        const data = response.data
        console.log(data)

        setRevenue(data.revenue)
        setProfit(data.profit)
        setCost(data.cost)
      } catch(error) {
        console.log('Error in today: ', error)
      } 
    }
    
    fetchData()
    const interval = setInterval(fetchData, 10000)

    return () => clearInterval(interval)
  }, [])
  
  return (
    <div className="today">
      <div className="grid-header"><h1>Today</h1></div>

          <div className="info-item">
            <h2>REVENUE</h2>
            <p>{revenue}€</p>
         </div>

         <div className="info-item">
            <h2>OPEARING COST</h2>
            <p>{cost}€</p>
         </div>  

         <div className="info-item">
            <h2>PROFIT</h2>
            <p>{profit}€</p>
         </div>  

    </div>
  )
}

export default Today