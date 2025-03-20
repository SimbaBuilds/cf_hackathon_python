export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  graphql_public: {
    Tables: {
      [_ in never]: never
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      graphql: {
        Args: {
          operationName?: string
          query?: string
          variables?: Json
          extensions?: Json
        }
        Returns: Json
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
  public: {
    Tables: {
      admin_actions: {
        Row: {
          action_type: string
          details: string | null
          id: number
          timestamp: string | null
          user_id: number | null
        }
        Insert: {
          action_type: string
          details?: string | null
          id?: number
          timestamp?: string | null
          user_id?: number | null
        }
        Update: {
          action_type?: string
          details?: string | null
          id?: number
          timestamp?: string | null
          user_id?: number | null
        }
        Relationships: []
      }
      answers: {
        Row: {
          answer: string
          correct: boolean
          id: number
          question_id: number
          quiz_id: number
          timestamp: string
          user_id: number
        }
        Insert: {
          answer: string
          correct: boolean
          id?: number
          question_id: number
          quiz_id: number
          timestamp?: string
          user_id: number
        }
        Update: {
          answer?: string
          correct?: boolean
          id?: number
          question_id?: number
          quiz_id?: number
          timestamp?: string
          user_id?: number
        }
        Relationships: [
          {
            foreignKeyName: "answers_question_id_fkey"
            columns: ["question_id"]
            isOneToOne: false
            referencedRelation: "question_bank_table"
            referencedColumns: ["id"]
          },
        ]
      }
      chat_history: {
        Row: {
          id: number
          messages: Json
          session_start: string | null
          user_id: number
        }
        Insert: {
          id?: number
          messages: Json
          session_start?: string | null
          user_id: number
        }
        Update: {
          id?: number
          messages?: Json
          session_start?: string | null
          user_id?: number
        }
        Relationships: []
      }
      chatbot_responses: {
        Row: {
          created_at: string | null
          id: number
          response: string
          user_id: number
        }
        Insert: {
          created_at?: string | null
          id?: number
          response: string
          user_id: number
        }
        Update: {
          created_at?: string | null
          id?: number
          response?: string
          user_id?: number
        }
        Relationships: []
      }
      conversations: {
        Row: {
          conversation_number: number
          id: string
          timestamp: string | null
          title: string | null
          user_id: string
        }
        Insert: {
          conversation_number: number
          id: string
          timestamp?: string | null
          title?: string | null
          user_id: string
        }
        Update: {
          conversation_number?: number
          id?: string
          timestamp?: string | null
          title?: string | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "conversations_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      curriculum_plans: {
        Row: {
          created_at: string | null
          description: string | null
          id: number
          plan_name: string
          status: string | null
          subjects: Json
          type: string
          user_id: number
        }
        Insert: {
          created_at?: string | null
          description?: string | null
          id?: number
          plan_name: string
          status?: string | null
          subjects: Json
          type?: string
          user_id: number
        }
        Update: {
          created_at?: string | null
          description?: string | null
          id?: number
          plan_name?: string
          status?: string | null
          subjects?: Json
          type?: string
          user_id?: number
        }
        Relationships: []
      }
      feedback: {
        Row: {
          comment: string
          id: number
          rating: number | null
          timestamp: string | null
          user_id: number
        }
        Insert: {
          comment: string
          id?: number
          rating?: number | null
          timestamp?: string | null
          user_id: number
        }
        Update: {
          comment?: string
          id?: number
          rating?: number | null
          timestamp?: string | null
          user_id?: number
        }
        Relationships: []
      }
      homework_table: {
        Row: {
          assignment: string
          details: string | null
          due_date: string | null
          id: number
          user_id: number
        }
        Insert: {
          assignment: string
          details?: string | null
          due_date?: string | null
          id?: number
          user_id: number
        }
        Update: {
          assignment?: string
          details?: string | null
          due_date?: string | null
          id?: number
          user_id?: number
        }
        Relationships: []
      }
      knowledge_updates: {
        Row: {
          id: number
          new_information: string
          topic_id: number
        }
        Insert: {
          id?: number
          new_information: string
          topic_id: number
        }
        Update: {
          id?: number
          new_information?: string
          topic_id?: number
        }
        Relationships: []
      }
      messages: {
        Row: {
          content: string | null
          conversation_id: string | null
          id: number
          role: string | null
          timestamp: string | null
          user_id: string
        }
        Insert: {
          content?: string | null
          conversation_id?: string | null
          id?: number
          role?: string | null
          timestamp?: string | null
          user_id: string
        }
        Update: {
          content?: string | null
          conversation_id?: string | null
          id?: number
          role?: string | null
          timestamp?: string | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "messages_conversation_id_fkey"
            columns: ["conversation_id"]
            isOneToOne: false
            referencedRelation: "conversations"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "messages_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      notifications: {
        Row: {
          id: number
          is_dismissed: boolean | null
          message: string
          timestamp: string | null
          user_id: number
        }
        Insert: {
          id?: number
          is_dismissed?: boolean | null
          message: string
          timestamp?: string | null
          user_id: number
        }
        Update: {
          id?: number
          is_dismissed?: boolean | null
          message?: string
          timestamp?: string | null
          user_id?: number
        }
        Relationships: []
      }
      performance_analytics: {
        Row: {
          average_score: number
          completion_rate: number
          difficulty_level: string | null
          id: number
          subject: string
        }
        Insert: {
          average_score: number
          completion_rate: number
          difficulty_level?: string | null
          id?: number
          subject: string
        }
        Update: {
          average_score?: number
          completion_rate?: number
          difficulty_level?: string | null
          id?: number
          subject?: string
        }
        Relationships: []
      }
      practice_tests_table: {
        Row: {
          answer_explanation: string | null
          choices: Json | null
          correct_answer: string | null
          difficulty: string | null
          domain: string | null
          equation: string | null
          figure_description: string | null
          id: number
          image: string | null
          practice_test: string | null
          question_content: string | null
          question_number: number | null
          skill: string | null
          sub_topic: string | null
          svg: string | null
          tabular_data: Json | null
          topic: string | null
          type: string | null
        }
        Insert: {
          answer_explanation?: string | null
          choices?: Json | null
          correct_answer?: string | null
          difficulty?: string | null
          domain?: string | null
          equation?: string | null
          figure_description?: string | null
          id?: number
          image?: string | null
          practice_test?: string | null
          question_content?: string | null
          question_number?: number | null
          skill?: string | null
          sub_topic?: string | null
          svg?: string | null
          tabular_data?: Json | null
          topic?: string | null
          type?: string | null
        }
        Update: {
          answer_explanation?: string | null
          choices?: Json | null
          correct_answer?: string | null
          difficulty?: string | null
          domain?: string | null
          equation?: string | null
          figure_description?: string | null
          id?: number
          image?: string | null
          practice_test?: string | null
          question_content?: string | null
          question_number?: number | null
          skill?: string | null
          sub_topic?: string | null
          svg?: string | null
          tabular_data?: Json | null
          topic?: string | null
          type?: string | null
        }
        Relationships: []
      }
      pt_backup: {
        Row: {
          answer_explanation: string | null
          choices: Json | null
          correct_answer: string | null
          difficulty: string | null
          domain: string | null
          equation: string | null
          figure_description: string | null
          id: number | null
          image: string | null
          practice_test: string | null
          question_content: string | null
          question_number: number | null
          skill: string | null
          sub_topic: string | null
          svg: string | null
          tabular_data: Json | null
          topic: string | null
          type: string | null
        }
        Insert: {
          answer_explanation?: string | null
          choices?: Json | null
          correct_answer?: string | null
          difficulty?: string | null
          domain?: string | null
          equation?: string | null
          figure_description?: string | null
          id?: number | null
          image?: string | null
          practice_test?: string | null
          question_content?: string | null
          question_number?: number | null
          skill?: string | null
          sub_topic?: string | null
          svg?: string | null
          tabular_data?: Json | null
          topic?: string | null
          type?: string | null
        }
        Update: {
          answer_explanation?: string | null
          choices?: Json | null
          correct_answer?: string | null
          difficulty?: string | null
          domain?: string | null
          equation?: string | null
          figure_description?: string | null
          id?: number | null
          image?: string | null
          practice_test?: string | null
          question_content?: string | null
          question_number?: number | null
          skill?: string | null
          sub_topic?: string | null
          svg?: string | null
          tabular_data?: Json | null
          topic?: string | null
          type?: string | null
        }
        Relationships: []
      }
      qb_back_up: {
        Row: {
          answer_explanation: string | null
          choices: Json | null
          correct_answer: string | null
          equation: string | null
          figure_description: string | null
          id: number | null
          image: string | null
          question_content: string | null
          question_number_in_subtopic: number | null
          sub_topic: string | null
          svg: string | null
          tabular_data: Json | null
          topic: string | null
          type: string | null
        }
        Insert: {
          answer_explanation?: string | null
          choices?: Json | null
          correct_answer?: string | null
          equation?: string | null
          figure_description?: string | null
          id?: number | null
          image?: string | null
          question_content?: string | null
          question_number_in_subtopic?: number | null
          sub_topic?: string | null
          svg?: string | null
          tabular_data?: Json | null
          topic?: string | null
          type?: string | null
        }
        Update: {
          answer_explanation?: string | null
          choices?: Json | null
          correct_answer?: string | null
          equation?: string | null
          figure_description?: string | null
          id?: number | null
          image?: string | null
          question_content?: string | null
          question_number_in_subtopic?: number | null
          sub_topic?: string | null
          svg?: string | null
          tabular_data?: Json | null
          topic?: string | null
          type?: string | null
        }
        Relationships: []
      }
      question_bank_table: {
        Row: {
          answer_explanation: string | null
          choices: Json | null
          correct_answer: string | null
          equation: string | null
          figure_description: string | null
          id: number
          image: string | null
          question_content: string | null
          question_number_in_subtopic: number | null
          sub_topic: string | null
          svg: string | null
          tabular_data: Json | null
          topic: string | null
          type: string | null
        }
        Insert: {
          answer_explanation?: string | null
          choices?: Json | null
          correct_answer?: string | null
          equation?: string | null
          figure_description?: string | null
          id?: number
          image?: string | null
          question_content?: string | null
          question_number_in_subtopic?: number | null
          sub_topic?: string | null
          svg?: string | null
          tabular_data?: Json | null
          topic?: string | null
          type?: string | null
        }
        Update: {
          answer_explanation?: string | null
          choices?: Json | null
          correct_answer?: string | null
          equation?: string | null
          figure_description?: string | null
          id?: number
          image?: string | null
          question_content?: string | null
          question_number_in_subtopic?: number | null
          sub_topic?: string | null
          svg?: string | null
          tabular_data?: Json | null
          topic?: string | null
          type?: string | null
        }
        Relationships: []
      }
      question_types: {
        Row: {
          question_type_id: number
          question_type_name: string
        }
        Insert: {
          question_type_id?: number
          question_type_name: string
        }
        Update: {
          question_type_id?: number
          question_type_name?: string
        }
        Relationships: []
      }
      reminders: {
        Row: {
          id: number
          message: string
          reminder_time: string
          user_id: number
        }
        Insert: {
          id?: number
          message: string
          reminder_time: string
          user_id: number
        }
        Update: {
          id?: number
          message?: string
          reminder_time?: string
          user_id?: number
        }
        Relationships: []
      }
      session_summaries: {
        Row: {
          chat_id: number
          highlights: Json
          id: number
        }
        Insert: {
          chat_id: number
          highlights: Json
          id?: number
        }
        Update: {
          chat_id?: number
          highlights?: Json
          id?: number
        }
        Relationships: []
      }
      test_attempts_table: {
        Row: {
          attempt_id: number
          created_at: string | null
          responses: Json
          status: string
          test_id: number
          user_id: number
        }
        Insert: {
          attempt_id?: number
          created_at?: string | null
          responses: Json
          status: string
          test_id: number
          user_id: number
        }
        Update: {
          attempt_id?: number
          created_at?: string | null
          responses?: Json
          status?: string
          test_id?: number
          user_id?: number
        }
        Relationships: [
          {
            foreignKeyName: "test_attempts_table_test_id_fkey"
            columns: ["test_id"]
            isOneToOne: false
            referencedRelation: "practice_tests_table"
            referencedColumns: ["id"]
          },
        ]
      }
      usage_analytics: {
        Row: {
          feature_name: string
          id: number
          last_used: string | null
          usage_count: number
        }
        Insert: {
          feature_name: string
          id?: number
          last_used?: string | null
          usage_count: number
        }
        Update: {
          feature_name?: string
          id?: number
          last_used?: string | null
          usage_count?: number
        }
        Relationships: []
      }
      user_messages: {
        Row: {
          content: string
          created_at: string | null
          id: number
          user_id: number
        }
        Insert: {
          content: string
          created_at?: string | null
          id?: number
          user_id: number
        }
        Update: {
          content?: string
          created_at?: string | null
          id?: number
          user_id?: number
        }
        Relationships: []
      }
      user_practice_tests: {
        Row: {
          completed_at: string | null
          practice_test_id: number
          score: number | null
          user_id: number
        }
        Insert: {
          completed_at?: string | null
          practice_test_id: number
          score?: number | null
          user_id: number
        }
        Update: {
          completed_at?: string | null
          practice_test_id?: number
          score?: number | null
          user_id?: number
        }
        Relationships: [
          {
            foreignKeyName: "user_practice_tests_practice_test_id_fkey"
            columns: ["practice_test_id"]
            isOneToOne: false
            referencedRelation: "practice_tests_table"
            referencedColumns: ["id"]
          },
        ]
      }
      user_progress: {
        Row: {
          id: number
          quiz_id: number
          score: number
          session_id: string | null
          timestamp: string | null
          user_id: number
        }
        Insert: {
          id?: number
          quiz_id: number
          score: number
          session_id?: string | null
          timestamp?: string | null
          user_id: number
        }
        Update: {
          id?: number
          quiz_id?: number
          score?: number
          session_id?: string | null
          timestamp?: string | null
          user_id?: number
        }
        Relationships: []
      }
      user_question_progress: {
        Row: {
          progress: number
          question_type_id: number
          user_id: string
        }
        Insert: {
          progress: number
          question_type_id: number
          user_id: string
        }
        Update: {
          progress?: number
          question_type_id?: number
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "user_question_progress_question_type_id_fkey"
            columns: ["question_type_id"]
            isOneToOne: false
            referencedRelation: "question_types"
            referencedColumns: ["question_type_id"]
          },
          {
            foreignKeyName: "user_question_progress_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      user_settings: {
        Row: {
          id: number
          setting: string
          setting_type: string
          user_id: number
        }
        Insert: {
          id?: number
          setting: string
          setting_type: string
          user_id: number
        }
        Update: {
          id?: number
          setting?: string
          setting_type?: string
          user_id?: number
        }
        Relationships: []
      }
      users: {
        Row: {
          access_token: string | null
          additional_info: Json | null
          created_at: string | null
          email: string
          full_name: string | null
          password_hash: string
          profile_picture: string | null
          role: string | null
          status: boolean | null
          token_type: string | null
          updated_at: string | null
          user_id: string
          username: string
        }
        Insert: {
          access_token?: string | null
          additional_info?: Json | null
          created_at?: string | null
          email: string
          full_name?: string | null
          password_hash: string
          profile_picture?: string | null
          role?: string | null
          status?: boolean | null
          token_type?: string | null
          updated_at?: string | null
          user_id: string
          username: string
        }
        Update: {
          access_token?: string | null
          additional_info?: Json | null
          created_at?: string | null
          email?: string
          full_name?: string | null
          password_hash?: string
          profile_picture?: string | null
          role?: string | null
          status?: boolean | null
          token_type?: string | null
          updated_at?: string | null
          user_id?: string
          username?: string
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      execute_ddl: {
        Args: {
          ddl_command: string
        }
        Returns: undefined
      }
      get_table_info: {
        Args: {
          p_table_name: string
        }
        Returns: {
          column_name: string
          data_type: string
          is_nullable: boolean
          column_default: string
        }[]
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type PublicSchema = Database[Extract<keyof Database, "public">]

export type Tables<
  PublicTableNameOrOptions extends
    | keyof (PublicSchema["Tables"] & PublicSchema["Views"])
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
        Database[PublicTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
      Database[PublicTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : PublicTableNameOrOptions extends keyof (PublicSchema["Tables"] &
        PublicSchema["Views"])
    ? (PublicSchema["Tables"] &
        PublicSchema["Views"])[PublicTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  PublicEnumNameOrOptions extends
    | keyof PublicSchema["Enums"]
    | { schema: keyof Database },
  EnumName extends PublicEnumNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = PublicEnumNameOrOptions extends { schema: keyof Database }
  ? Database[PublicEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : PublicEnumNameOrOptions extends keyof PublicSchema["Enums"]
    ? PublicSchema["Enums"][PublicEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof PublicSchema["CompositeTypes"]
    | { schema: keyof Database },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof Database
  }
    ? keyof Database[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends { schema: keyof Database }
  ? Database[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof PublicSchema["CompositeTypes"]
    ? PublicSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never


    //re-run: cd .. && supabase gen types typescript --linked > app/schemas.ts