/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chart.jsx                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/12/27 13:41:19 by jmykkane          #+#    #+#             */
/*   Updated: 2023/12/27 19:16:04 by jmykkane         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

import { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import axios from 'axios'
import 'chart.js/auto'

const Chart = () => {
  const [data, setData] = useState({ labels: [], datasets: [], })

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/data/month')
        setData(response.data)
      } catch(error) {
        console.log('Error in today: ', error)
      } 
      console.log(data)
    }

    fetchData()
  }, [])
  
  
  return (
    <div className='chart'>
      {Object.keys(data).length > 0 && (
        <Line
          data={data}
          options={{
            plugins: {
              title: {
                display: true,
                text: 'Month to date:',
              },
            },
          }}
        />
      )}
    </div>
  )
}

export default Chart