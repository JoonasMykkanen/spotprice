/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   App.js                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/12/26 08:57:02 by jmykkane          #+#    #+#             */
/*   Updated: 2023/12/26 09:21:45 by jmykkane         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

import Grid from './Components/grid'
import Nav from './Components/nav'
import './App.css'

function App() {
  return (
    <div className='App'>
      <Nav />
      <Grid />
    </div>
  )
}

export default App
