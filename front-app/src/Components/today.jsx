/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   today.jsx                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/12/26 12:39:18 by jmykkane          #+#    #+#             */
/*   Updated: 2023/12/26 13:40:42 by jmykkane         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

const Today = () => {
  
  return (
    <div className="today">
      <div className="grid-header"><h1>Today</h1></div>

          <div className="info-item">
            <h2>REVENUE</h2>
            <p>eur</p>
         </div>

         <div className="info-item">
            <h2>OPEARING COST</h2>
            <p>eur</p>
         </div>  

         <div className="info-item">
            <h2>PROFIT</h2>
            <p>eur</p>
         </div>  

    </div>
  )
}

export default Today