# Data Dictionary - Hotel Booking Dataset

**Version**: 1.0  
**Last Updated**: 2026-05-10  
**Author**: Nwaeke Calixtus, Esq  
**License**: MIT

---

## Overview
This document describes the schema and characteristics of the hotel booking dataset. All fields are defined with their data types, value ranges, and business meanings.

## Core Fields

### Booking Information

| Field | Type | Format | Range | Description |
|-------|------|--------|-------|-------------|
| `booking_id` | Integer | Unique ID | 1 - 10,000,000 | Unique identifier for each booking |
| `hotel_id` | Integer | Unique ID | 1 - 1,000,000 | Unique identifier for each hotel property |
| `hotel_name` | String | Text | Max 255 chars | Official name of the hotel property |
| `check_in_date` | DateTime | YYYY-MM-DD | 2015-01-01+ | Guest arrival date/time |
| `check_out_date` | DateTime | YYYY-MM-DD | check_in_date + | Guest departure date/time |
| `booking_date` | DateTime | YYYY-MM-DD | check_in_date - | Date when booking was made |

### Guest Information

| Field | Type | Format | Range | Description |
|-------|------|--------|-------|-------------|
| `num_guests` | Integer | Count | 1 - 20 | Number of guests in booking |
| `num_adults` | Integer | Count | 0 - 20 | Number of adults in booking |
| `num_children` | Integer | Count | 0 - 10 | Number of children in booking |
| `guest_nationality` | String | ISO 3166-1 | 2-letter code | Guest country of origin |
| `guest_email` | String | RFC 5322 | Valid email | Guest contact email |
| `guest_phone` | String | E.164 | +1-XXX-XXX-XXXX | Guest contact phone |

### Room Information

| Field | Type | Format | Range | Description |
|-------|------|--------|-------|-------------|
| `room_type` | String | Categorical | Single, Double, Suite, etc. | Type of room booked |
| `num_rooms` | Integer | Count | 1 - 10 | Number of rooms in booking |
| `room_rate` | Float | Currency | 0.00 - 999,999.99 | Price per room per night (USD) |
| `total_price` | Float | Currency | 0.00 - 999,999.99 | Total booking price (USD) |
| `has_special_requests` | Boolean | Yes/No | True/False | Whether booking has special requests |
| `special_requests` | String | Text | Max 1000 chars | Details of guest special requests |

### Booking Status

| Field | Type | Format | Values | Description |
|-------|------|--------|--------|-------------|
| `booking_status` | String | Categorical | Confirmed, Cancelled, No-show, Completed | Current status of booking |
| `cancellation_date` | DateTime | YYYY-MM-DD | null or valid date | Date booking was cancelled |
| `is_cancelled` | Boolean | Flag | True/False | Whether booking was cancelled |
| `cancellation_reason` | String | Text | Max 500 chars | Reason for cancellation if applicable |

### Payment Information

| Field | Type | Format | Values | Description |
|-------|------|--------|--------|-------------|
| `payment_method` | String | Categorical | Credit Card, PayPal, Bank Transfer, etc. | Payment method used |
| `payment_status` | String | Categorical | Pending, Completed, Failed, Refunded | Status of payment |
| `is_paid` | Boolean | Flag | True/False | Whether full payment received |
| `deposit_amount` | Float | Currency | 0.00 - total_price | Deposit/advance payment (USD) |

### Property Information

| Field | Type | Format | Range | Description |
|-------|------|--------|-------|-------------|
| `hotel_location` | String | City, Country | Max 100 chars | Geographic location of hotel |
| `hotel_stars` | Integer | Rating | 1 - 5 | Star rating of hotel (if applicable) |
| `hotel_type` | String | Categorical | Luxury, Business, Budget, Resort, etc. | Classification of hotel |
| `checkin_type` | String | Categorical | Selfcheck-in, Standard, VIP | Type of check-in experience |

### Behavioral Flags

| Field | Type | Format | Values | Description |
|-------|------|--------|--------|-------------|
| `is_repeat_guest` | Boolean | Flag | True/False | Whether guest has booked before |
| `previous_bookings` | Integer | Count | 0 - 1000 | Number of prior bookings at this hotel |
| `is_corporate_booking` | Boolean | Flag | True/False | Whether booking is from corporate account |
| `lead_time_days` | Integer | Days | 0 - 730 | Days between booking date and check-in |

---

## Data Quality Standards

### Null Values
- All ID fields must have values (no nulls)
- No nulls allowed in dates, guest count, or prices
- Nullable fields: `special_requests`, `cancellation_reason`, `guest_phone`

### Validation Rules
- `check_out_date` > `check_in_date`
- `check_in_date` >= `booking_date`
- `num_guests` > 0
- `room_rate` >= 0
- `lead_time_days` >= 0
- Guest email must be valid RFC 5322 format

### Cleaning Procedures
1. Remove rows with `num_guests = 0`
2. Remove duplicate bookings (based on booking_id)
3. Coerce numeric fields to float/integer
4. Parse dates to ISO 8601 format
5. Normalize string fields (trim whitespace, lowercase categorical)
6. Impute missing values per business rules

---

## Derived Fields (For Analysis)

| Field | Formula | Purpose |
|-------|---------|---------|
| `length_of_stay` | check_out_date - check_in_date | Number of nights booked |
| `total_days_booked` | length_of_stay * num_rooms | Total room-nights for analysis |
| `average_daily_rate` | total_price / length_of_stay | Revenue per night |
| `booking_month` | MONTH(booking_date) | Seasonal analysis |
| `season` | CASE WHEN month IN (12,1,2)... | High/Low season classification |
| `is_weekend_checkin` | DAYOFWEEK(check_in_date) IN (6,7) | Weekend vs Weekday analysis |

---

## Statistical Summaries

### Room Rate Distribution (Historical)
- **Mean**: $152.45
- **Median**: $125.00
- **Std Dev**: $89.34
- **Min**: $15.00
- **Max**: $2,500.00
- **Q1**: $75.00
- **Q3**: $200.00

### Guest Count Distribution
- **Mean**: 2.34 guests
- **Median**: 2 guests
- **Mode**: 2 guests
- **Range**: 1 - 12 guests

### Lead Time (Days)
- **Mean**: 92.5 days
- **Median**: 69 days
- **Range**: 0 - 730 days

---

## Data Governance

### Access Restrictions
- Contains personally identifiable information (PII)
- Subject to GDPR and CCPA regulations
- Authorized users only
- Use for analysis purposes only

### Data Retention
- Raw data: Retain for 7 years per business requirements
- Processed data: Retain for 3 years per privacy policy
- Deletion: Follow secure data destruction protocols

### License & Attribution
This dataset and all analyses derived from it are subject to the MIT License.  
Copyright © 2026 Nwaeke Calixtus, Esq. All rights reserved.

---

## References
- ISO 8601 (Date/Time Format)
- RFC 5322 (Email Format)
- E.164 (Phone Format)
- GDPR Compliance: https://gdpr-info.eu/
- CCPA Compliance: https://oag.ca.gov/privacy/ccpa

---

**Questions?** Contact: calixtusnwaeke@gmail.com
