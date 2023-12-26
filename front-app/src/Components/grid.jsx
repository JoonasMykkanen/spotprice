/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   grid.jsx                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/12/26 09:20:37 by jmykkane          #+#    #+#             */
/*   Updated: 2023/12/26 13:38:30 by jmykkane         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

import Stats from './stats'
import Today from './today'

const Grid = () => {
  return (
    <div className="grid">
      <div className="grid-container">
        <div className="grid-item horizontal">

        </div>
        <div className="grid-item square">
          <Stats />
        </div>
        <div className="grid-item vertical">
          
        </div>
        <div className="grid-item square">
          <Today />
        </div>
        <div className="grid-item horizontal">
          
        </div>
      </div>
    </div>
  )
}

export default Grid