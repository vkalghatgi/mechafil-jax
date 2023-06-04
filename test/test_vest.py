import unittest
from datetime import date, timedelta

import mechafil_jax.vesting as jax_vest
import mechafil.vesting as np_vest
import mechafil.data as data

import numpy as np

class TestVesting(unittest.TestCase):
    def test_vesting(self):
        # setup data access
        # TODO: better way to do this?
        data.setup_spacescope('/Users/kiran/code/filecoin-mecha-twin/kiran_spacescope_auth.json')

        start_date = date(2021, 3, 16)
        forecast_length = 5*365
        current_date = date.today() - timedelta(days=2)
        end_date = current_date + timedelta(days=forecast_length)

        # get base vesting amount that is needed for vesting calculations
        start_vested_amt = int(data.get_vested_amount(start_date))
        
        np_vesting_df = np_vest.compute_vesting_trajectory_df(start_date, end_date)
        jax_vesting_dict = jax_vest.compute_vesting_trajectory(
            np.datetime64(start_date), 
            np.datetime64(end_date), 
            start_vested_amt
        )

        # compare
        self.assertTrue(np.allclose(np.asarray(np_vesting_df['total_vest'].values), 
                                    np.asarray(jax_vesting_dict['total_vest'])))
        
if __name__ == '__main__':
    unittest.main()