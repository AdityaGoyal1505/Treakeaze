classDiagram
    %% Core User and Conference
    class User {
        +email
        +is_verified
        +otp
    }
    
    class Conference {
        +name
        +acronym
        +status: [upcoming, live, completed]
        +start_date
        +deadline_settings
        +blind_review: bool
    }

    class Track {
        +name
        +track_id
    }
    
    %% Roles linking User to Conference
    class UserConferenceRole {
        +role: [chair, author, reviewer, pc_member]
    }
    
    %% Paper Submission
    class Paper {
        +title
        +abstract
        +file
        +status: [submitted, under_review, accepted...]
        +paper_id
        +plagiarism_percentage
    }
    
    class Author {
        +first_name
        +last_name
        +affiliation
        +is_corresponding
    }

    %% Review System
    class Review {
        +decision: [accept, reject]
        +rating: int
        +confidence: int
        +comments
    }
    
    class ReviewInvite {
        +status: [pending, accepted, declined]
    }

    %% Relationships
    User "1" -- "*" Conference : organizes (as Chair)
    User "1" -- "*" UserConferenceRole : has role
    Conference "1" -- "*" UserConferenceRole : defines roles
    
    Conference "1" -- "*" Track : has
    Track "1" -- "*" Paper : classifies
    
    Conference "1" -- "*" Paper : receives
    User "1" -- "*" Paper : submits (as Author)
    Paper "1" -- "*" Author : lists (Co-authors)
    
    Paper "1" -- "*" Review : gets evaluated by
    User "1" -- "*" Review : writes (as Reviewer)
    
    Conference "1" -- "*" ReviewInvite : sends
    User "1" -- "*" ReviewInvite : receives
    
    Conference "1" -- "1" ConferenceAdminSettings : configured by