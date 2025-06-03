/*
with

employees as (
	select * from employees 
)



payroll_summary as (
	select
		employee_id,
		max(pay_period_end) as last_payroll_date,
		sum(case when year(pay_period_start) = year(current_date) then gross_pay end) as ytd_gross_pay
		sum(case when year(pay_period_start) = year(current_date) then net_pay end) as ytd_net_pay
		
	from payroll_record
	left join payroll_statuses on
		payroll statuses.id = payroll_record.id
)
*/
with 

customer_account_summary as (
	select
		customers.id as customer_id,
		customers.name as customer_name,
		case
			when customers.active then 'Active'
			else 'Inactive'
		end as customer_status
		accounts.industry,
		accounts.employees as total_employee_count,
		accounts.subscription_start,
		accounts.subscription_end
		case
			when accounts.subscription_end is null then 'Active'
			when accounts.subscription_end > current_timestamp then 'Active'
			else 'Inactive'
		end as subscription_status
	from customers
	left join accounts on
		accounts.customer_id = customers.id
),

department_hierarchy as (
	with recursive dept_org as (
		select
			customer_id,
			departments.id,
			departments.name as department_name,
			departments.created_at
			departments.updated_at
			case
				when departments.active then 'Active'
				else 'Inactive'
			end as department_status
		from departments_base
		where parent_id is null
		
		union all
		
		select
			departments.id,
			departments.name as department_name,
			departments.created_at
			departments.updated_at
			case
				when departments.active then 'Active'
				else 'Inactive'
			end as department_status
		from departments_branches
		join dept_org on 
			departments_branches.parent_id = departments_base.id
			and departments_branches.customer_id = departments_base.customer_id
	)
	select * from dept_org
),



employees as (
	select
		employees.id,
		employees.customer_id,
		concat_ws(' ', employees.first_name, employees.last_name) as employee_name,
		work_email as employee_email,
		employees.job_title,
		employees.created_at::date as created_at,
		employees.hired_at::date as hire_date,
		employees.terminated_at::date as term_date,
		employees.salary,
		employees.salary_frequency,
		employees.last_login_at as last_login_timestamp,
		employee_statuses.key as employee_status
	from employees
	left join employee_statuses on
		employee_statuses.id = employees.status_id
)

	select
		customer_account_summary.customer_id,
		customer_account_summary.customer_name,
		customer_account_summary.customer_status,
		customer_account_summary.subscription_start,
		customer_account_summary.subscription_end,
		customer_account_summary.subscription_status,
		-- department
		departments.name as department_name,
		departments.department_status,
		-- employee details
		employees.employee_id,
		employees.employee_name,
		employees.employee_email,
		employees.hire_date,
		employees.term_date,
		employees.job_title,
		employees.salary,
		employee.employee_status,
		-- (coalesce(employee.term_date,current_date) - employee.hire_date) as employee_tenure
		-- role detail
		roles.status as role_status,
		string_agg(distinct roles.key,', ') as roles,
		-- case
		-- 	when roles.updated_at = roles.created_at then current_date - roles.created_at 
		-- 	else roles.updated_at - roles.created_at
		-- end as role_tenure,
		--booleans
		bool_or(case when key ='admin' then true else false end) as is_admin,
		bool_or(case when key ='employee' then true else false end) as is_employee,
		bool_or(case when key ='fulltime' then true else false end) as is_fulltime,
		bool_or(case when key ='parttime' then true else false end) as is_parttime,
		bool_or(case when key ='intern' then true else false end) as is_intern,
		bool_or(case when key ='contractor' then true else false end) as is_contractor
	from customer_account_summary
	left join department_hierarchy.customer_id = customer_account_summary.customer_id
	left join employees on
		employees.customer_id = customer_account_summary.customer_id
		and employees.department_id = department_hierarchy.id
	left join roles on
		roles.employee_id = employees.id
	
	
