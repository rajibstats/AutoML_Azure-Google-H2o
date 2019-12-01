# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import pickle
import numpy as np
import pandas as pd
import azureml.train.automl
from sklearn.externals import joblib
from azureml.core.model import Model

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


input_sample = pd.DataFrame(data=[{"fund_id":11554,"stock_id":357,"Quarter":2,"sharevalue":49002,"stock_price":28.19,"Aging":781,"Cap_Size":"MegaCap","IsOwner":1,"Year":2018,"Cap_SizeID":5,"industry":"Banks","Sector_ID":4,"ActivePassive":1,"fund_type":3,"Investor Style":9999,"AUM":1,"Turnover":4,"Region":13,"asset_turn":0.0095,"book_val_per_share":26.388,"curr_ratio":0.905028366,"day_sale_rcv":38.543,"ebit_margin":21.9015,"ebitda_margin":30.6461,"free_cash_flow":33836,"free_cash_flow_per_share":3.2821,"gross_margin":0.8273199649,"invty_turn":1.4727,"loan_loss_reserve":1.7043,"lterm_debt_cap":0.4617,"non_perform_asset_tot_loan":0.0066,"oper_cash_flow_per_share":3.2821,"oper_profit_margin":0.3109631148,"pretax_profit_margin":39.0139,"profit_margin":29.6851,"rcv_turn":2.3351,"ret_asset":0.296,"ret_equity":2.8145,"ret_invst":1.3822,"ret_tang_equity":3.4743,"tot_debt_tot_equity":2.0141,"tot_share_holder_equity":264216,"income_aft_tax":6784,"pre_tax_income":8498,"tot_liab":2027454,"tot_liab_share_holder_equity":2291670,"tang_stock_holder_equity":195265,"tot_comm_equity":241035,"cash_flow_invst_activity":-20869,"incr_decr_cash":13765,"cash_flow_oper_activity":33836,"cash_flow_fin_activity":1517,"tot_deprec_amort_cash_flow":1933,"tot_change_asset_liab":14022,"dilution_factor":28.9224,"tot_provsn_income_tax":1714,"basic_net_eps":0.64,"diluted_net_eps":0.63,"avg_b_shares":10181.7,"avg_d_shares":10309.4,"comm_stock_net":128822,"net_change_prop_plant_equip":-2468.0,"retain_earn_accum_deficit":125546,"tot_revnu":27328,"tot_oper_exp":18830,"net_prop_plant_equip":9537,"ebit":3842.0,"net_comm_equity_issued_repurch":-9823,"ebitda":6367.0,"tot_non_oper_income_exp":-60.0,"addtl_paid_in_cap":60685.0,"debt_issue_retire_net_tot":14114,"cash_sterm_invst":609317,"acct_pay":1309691,"stock_based_compsn":877.0,"tot_curr_asset":1599415,"tot_curr_liab":1767254,"rcv_tot":9138.0,"tot_sell_gen_admin_exp":14111,"non_oper_int_exp":672.0,"cost_good_sold":4719,"tot_lterm_debt":226595,"other_non_curr_liab":33605.0,"gross_profit":22609,"oper_income":8498,"cap_expense":-3349.0,"eps_amt_diff_surp":0.0,"eps_mean_est":0.63,"eps_pct_diff_surp":0.0,"sales_amt_diff_surp":136.58,"sales_mean_est":22212.52,"sales_pct_diff_surp":0.61,"tot_invst_cap":121209.0,"tot_debt":532148}])
output_sample = np.array([0])


def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = Model.get_model_path(model_name = 'model (13).pkl')
    model = joblib.load(model_path)


@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))
def run(data):
    try:
        result = model.predict(data)
        return result.tolist()
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
    return json.dumps({"result": result.tolist()})
