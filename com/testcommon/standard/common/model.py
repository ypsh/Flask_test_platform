# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, String, text, Date
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Product(Base):
    __tablename__ = 'product'

    product_id = Column(BIGINT(20), primary_key=True, comment='产品id')
    project_code = Column(String(32), comment='项目编码')
    product_no = Column(String(32), comment='产品编码')
    loan_usage = Column(String(1024), comment='资金用途 多选，以逗号分隔')
    upload_cert = Column(INTEGER(11), server_default=text("'0'"), comment='是否强制上传贷款凭证 1-强制上传，0-不强制上传')
    credit_cycle_type = Column(String(32), server_default=text("'clear'"), comment='额度循环类型 详见数据字典-额度循环类型')
    multi_loan = Column(INTEGER(11), server_default=text("'1'"), comment='是否多笔借款 1-允许，0-不允许')
    supported_pay_way = Column(String(32),comment='支持的还款方式 详见数据字典-还款方式')
    credit_upper_limit = Column(BIGINT(20), comment='额度上限')
    credit_lower_limit = Column(BIGINT(20), comment='额度下限')
    loan_upper_limit = Column(BIGINT(20), comment='单笔借款上限')
    loan_lower_limit = Column(BIGINT(20), comment='单笔借款下限')
    year_rate_upper_limit = Column(DECIMAL(32, 10), comment='年利率上限')
    year_rate_lower_limit = Column(DECIMAL(32, 10), comment='年利率下限')
    pnlt_rate_float_percent = Column(DECIMAL(32, 10), comment='罚息利率上浮')
    year_rate_total_upper_limit = Column(DECIMAL(32, 10), comment='总年化利率上限 年利率+罚息利率<总年化利率上限')
    pnlt_int_base = Column(String(32), comment='罚息计算基准 详见数据字典-罚息计算基准')
    int_calc_type = Column(String(128), comment='计息方式 多选，逗号分隔，详见数据字典-计息方式')
    accrual_type = Column(String(32), comment='计提方式 详见数据字典-计提方式')
    loan_step = Column(BIGINT(20), comment='借款步长金额')
    reversal_plan_id = Column(INTEGER(11), comment='冲销方案')
    term = Column(String(128), comment='产品期限 多选，以逗号分隔，如：3，6，9，12')
    repay_day = Column(String(1024),
                       comment='账单日规则代码 {"1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","7":"7","8":"8","9":"9","10":"10","11":"11","12":"12","13":"13","14":"14","15":"15","16":"16","17":"17","18":"18","19":"19","20":"20","21":"21","22":"22","23":"23","24":"24","25":"25","26":"26","27":"27","28":"28","29":"29","30":"30","31":"31"}')
    year_type = Column(String(32), comment='计息基准年 详见数据字典-计息基准年')
    month_type = Column(String(32), comment='计息基准月 详见数据字典-计息基准月')
    grace_type = Column(String(32), comment='宽限期类型 详见数据字典-宽限期类型')
    grace_day = Column(INTEGER(11), comment='宽限天数 宽限类型为day时使用')
    grace_last_term = Column(INTEGER(11), comment='最后一期是否有宽限期 1-有宽限期，0-没有宽限期')
    prepay_type = Column(String(128), comment='提前还款类型 多选，逗号分隔，详见数据字典-提前还款类型')
    prepay_int_type = Column(String(32), comment='提前还款收息方式 详见数据字典-提前还款收息方式')
    prepay_lower_limit = Column(BIGINT(20), comment='提前还款最低金额')
    prepay_repay_plan_type = Column(String(32), server_default=text("'recal'"), comment='提前还款还款计划变更方式 recal-重算')
    grace_pnlt_int_type = Column(String(32), server_default=text("'no_pnlt_int'"), comment='宽限期罚息处理方式 no_pnlt_int-无罚息')
    fee_type = Column(String(32), server_default=text("'nofee'"), comment='手续费类型 nofee-无手续费')
    status = Column(String(32), server_default=text("'valid'"), comment='状态 valid-有效，invalid-无效')
    version = Column(INTEGER(11), comment='版本号')
    created_by = Column(String(32), comment='创建人')
    create_time = Column(DateTime, comment='创建时间')
    update_by = Column(String(32), comment='更新人')
    updated_time = Column(DateTime, comment='更新时间')

class CoreSysDate(Base):
    __tablename__ = 'core_sys_date'

    oid = Column(INTEGER(11), primary_key=True, comment='主键 不做业务逻辑')
    project_code = Column(String(32), nullable=False, comment='项目编号')
    core_sys_date = Column(Date, nullable=False, comment='核心时间')
    core_sys_status = Column(String(32), nullable=False, comment='核心状态 normal:正常 running:跑批中')
    create_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
