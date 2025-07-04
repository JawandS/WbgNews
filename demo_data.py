"""
Demo data loader for testing the meeting agenda system
"""

from datetime import datetime, timedelta
import random

def get_demo_meetings():
    """Generate demo meeting data for testing"""
    base_date = datetime.now() - timedelta(days=30)
    
    williamsburg_meetings = [
        {
            'meeting_date': (base_date + timedelta(days=2)).date(),
            'meeting_title': 'Williamsburg City Council Regular Meeting - Budget Review',
            'original_url': 'https://williamsburg.civicweb.net/Portal/MeetingDetails.aspx?ID=1234',
            'agenda_content': """
WILLIAMSBURG CITY COUNCIL
REGULAR MEETING AGENDA
July 2, 2025

1. CALL TO ORDER

2. APPROVAL OF MINUTES
   - June 18, 2025 Regular Meeting

3. PUBLIC COMMENT PERIOD

4. OLD BUSINESS
   A. Second Reading: Ordinance 2025-07 - Zoning Amendment for Historic District
   B. Resolution 2025-15 - Street Improvement Project Funding

5. NEW BUSINESS
   A. First Reading: Budget Amendment for FY 2025-26
      - Proposed increase in parks and recreation funding by $150,000
      - New allocation for downtown streetscape improvements: $300,000
      - Enhanced funding for historic preservation grants: $75,000
   
   B. Discussion: New Community Center Expansion
      - Architect presentations for proposed 5,000 sq ft addition
      - Estimated cost: $2.2 million
      - Proposed funding through municipal bonds
   
   C. Resolution 2025-16 - Traffic Calming Measures on Duke of Gloucester Street
      - Installation of speed bumps and enhanced crosswalks
      - Estimated cost: $45,000

6. DEPARTMENT REPORTS
   A. Public Works - Summer road maintenance schedule
   B. Parks & Recreation - Summer program enrollment update
   C. Planning & Zoning - Recent development applications

7. MAYOR'S REPORT
   - Update on tourism recovery post-pandemic
   - Upcoming Independence Day celebration logistics

8. COUNCIL MEMBER REPORTS

9. CLOSED SESSION (if needed)

10. ADJOURNMENT

Meeting materials available at City Hall and online at williamsburg.gov
            """,
            'source': 'williamsburg'
        },
        {
            'meeting_date': (base_date + timedelta(days=16)).date(),
            'meeting_title': 'Williamsburg Planning Commission - Development Review',
            'original_url': 'https://williamsburg.civicweb.net/Portal/MeetingDetails.aspx?ID=1235',
            'agenda_content': """
WILLIAMSBURG PLANNING COMMISSION
MEETING AGENDA
July 16, 2025

1. CALL TO ORDER & ROLL CALL

2. APPROVAL OF MINUTES

3. PUBLIC HEARINGS
   A. Case PL-2025-08: Special Use Permit for Boutique Hotel
      - Location: 315 Richmond Road
      - Applicant: Colonial Hospitality LLC
      - Proposed 45-room boutique hotel with restaurant
      - Parking variance requested

   B. Case PL-2025-09: Subdivision Amendment
      - Williamsburg Commons Phase III
      - Addition of 12 townhome units
      - Infrastructure impact assessment required

4. ADMINISTRATIVE ITEMS
   A. Staff Report: Comprehensive Plan Update Progress
   B. Review of Historic District Design Guidelines
   C. Parking Study Results - Downtown District

5. NEW BUSINESS
   A. Discussion: Short-term Rental Regulations
      - Current ordinance review
      - Impact on housing availability
      - Proposed amendments for consideration

6. STAFF REPORTS
   - Building permit activity summary
   - Code enforcement updates
   - Upcoming zoning workshops

7. COMMISSION COMMENTS

8. ADJOURNMENT

Next meeting: August 6, 2025
            """,
            'source': 'williamsburg'
        }
    ]
    
    jamescity_meetings = [
        {
            'meeting_date': (base_date + timedelta(days=9)).date(),
            'meeting_title': 'James City County Board of Supervisors Regular Meeting',
            'original_url': 'https://www.jamescitycountyva.gov/AgendaCenter/ViewFile/Agenda/_07092025-123',
            'agenda_content': """
JAMES CITY COUNTY
BOARD OF SUPERVISORS
REGULAR MEETING AGENDA
July 9, 2025

1. CALL TO ORDER

2. ROLL CALL

3. MOMENT OF SILENCE

4. PLEDGE OF ALLEGIANCE

5. PUBLIC COMMENT

6. PRESENTATIONS
   A. Annual Financial Report for FY 2024
   B. James City County Police Department Crime Statistics Update

7. BOARD CONSIDERATION
   A. Resolution R-25-15: Appropriation for School Technology Upgrades
      - $850,000 for new classroom computers and networking equipment
      - Federal ESSER funds utilization
   
   B. Ordinance O-25-08: Fire Protection Impact Fee Amendment
      - Adjustment to current fee schedule
      - Support for new fire station construction in the Toano area
   
   C. Contract Award: Route 5 Corridor Improvement Project
      - Selected contractor: Virginia Infrastructure Solutions
      - Project value: $3.2 million
      - Expected completion: Spring 2026

8. PLANNING COMMISSION RECOMMENDATIONS
   A. Case SUP-25-04: Solar Energy Facility
      - 150-acre solar farm on Centerville Road
      - Conditional approval with landscaping requirements
   
   B. Zoning Ordinance Amendment: Accessory Dwelling Units
      - Allowing ADUs in certain residential districts
      - Maximum size restrictions: 800 square feet

9. BOARD REQUESTS AND DIRECTIVES

10. COUNTY ADMINISTRATOR'S REPORT
    - Update on broadband expansion project
    - Tourism revenue quarterly report
    - Capital improvement project status

11. BOARD MEMBER REPORTS

12. CLOSED SESSION (Personnel and Legal Matters)

13. ADJOURNMENT

Meeting materials: jamescitycountyva.gov/AgendaCenter
            """,
            'source': 'jamescity'
        },
        {
            'meeting_date': (base_date + timedelta(days=23)).date(),
            'meeting_title': 'James City County Planning Commission Meeting',
            'original_url': 'https://www.jamescitycountyva.gov/AgendaCenter/ViewFile/Agenda/_07232025-456',
            'agenda_content': """
JAMES CITY COUNTY PLANNING COMMISSION
MEETING AGENDA
July 23, 2025

1. CALL TO ORDER

2. ROLL CALL

3. PUBLIC COMMENT

4. PLANNING DIRECTOR'S REPORT

5. COMMITTEE/COMMISSION REPORTS

6. PUBLIC HEARINGS
   A. Case Z-25-03: Rezoning Application
      - Property: 2847 Pocahontas Trail (45.3 acres)
      - Current zoning: A-1, Agricultural
      - Proposed zoning: R-2, General Residential
      - Applicant: Riverside Development Company
      - Proposed: 89 single-family homes
   
   B. Case SUP-25-06: Conditional Use Permit
      - Property: 4521 Monticello Avenue
      - Proposed use: Commercial kennel and pet daycare
      - Special conditions regarding noise mitigation
      - Operating hours: 6 AM to 8 PM

7. REGULAR AGENDA
   A. Master Plan Amendment Discussion
      - Land Use designation changes in Norge area
      - Community input session results
   
   B. Williamsburg Area Transit Authority Updates
      - Proposed new bus routes
      - Grant funding opportunities
   
   C. Economic Development Authority Quarterly Report
      - New business attraction efforts
      - Industrial park occupancy rates

8. PLANNING COMMISSION CONSIDERATIONS
   A. Draft Amendments to Subdivision Ordinance
      - Stormwater management requirements
      - Tree preservation standards
   
   B. Rural Lands Committee Recommendations
      - Agricultural preservation incentives
      - Rural character protection measures

9. ADJOURNMENT

Next meeting: August 13, 2025
            """,
            'source': 'jamescity'
        }
    ]
    
    return williamsburg_meetings + jamescity_meetings
