"""
Gemini API Integration Module
Handles all interactions with Google's Gemini API for AI-powered features
"""

import os
import json
from typing import Optional, Dict, List, Any
import google.generativeai as genai

class GeminiAIClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini AI client
        
        Args:
            api_key (str, optional): API key for Gemini. Defaults to env variable.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_code(self, code_snippet: str, language: str = "javascript") -> Dict[str, Any]:
        """
        Analyze code for bugs and improvements
        
        Args:
            code_snippet (str): Code to analyze
            language (str): Programming language
            
        Returns:
            dict: Analysis results with bugs, improvements, and best practices
        """
        prompt = f"""
        Analyze this {language} code for:
        1. Potential bugs
        2. Performance improvements
        3. Security vulnerabilities
        4. Best practices violations
        
        Code:
        ```{language}
        {code_snippet}
        ```
        
        Provide structured feedback as JSON.
        """
        
        response = self.model.generate_content(prompt)
        return json.loads(response.text)
    
    def generate_documentation(self, code: str, language: str = "javascript") -> str:
        """
        Generate comprehensive documentation for code
        
        Args:
            code (str): Source code
            language (str): Programming language
            
        Returns:
            str: Generated documentation
        """
        prompt = f"""
        Generate detailed documentation for this {language} code:
        
        ```{language}
        {code}
        ```
        
        Include:
        - Function descriptions
        - Parameter explanations
        - Return value descriptions
        - Usage examples
        - Edge cases
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def refactor_suggestion(self, code: str, language: str = "javascript") -> Dict[str, str]:
        """
        Get refactoring suggestions
        
        Args:
            code (str): Source code
            language (str): Programming language
            
        Returns:
            dict: Original code and refactored version
        """
        prompt = f"""
        Suggest refactoring for this {language} code to make it:
        1. More readable
        2. More maintainable
        3. More efficient
        
        Code:
        ```{language}
        {code}
        ```
        
        Provide refactored code and explain the improvements.
        """
        
        response = self.model.generate_content(prompt)
        return {
            "suggestions": response.text,
            "original": code
        }
    
    def code_review(self, code: str, language: str = "javascript") -> Dict[str, Any]:
        """
        Perform comprehensive code review
        
        Args:
            code (str): Source code
            language (str): Programming language
            
        Returns:
            dict: Detailed code review findings
        """
        prompt = f"""
        Perform a comprehensive code review of this {language} code:
        
        ```{language}
        {code}
        ```
        
        Evaluate:
        1. Code quality (scale 1-10)
        2. Readability
        3. Performance
        4. Security
        5. Testing considerations
        6. Documentation quality
        7. Best practices adherence
        
        Provide JSON response with scores and recommendations.
        """
        
        response = self.model.generate_content(prompt)
        return json.loads(response.text)


# Example usage
if __name__ == "__main__":
    client = GeminiAIClient()
    
    sample_code = """
    function fibonacci(n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    """
    
    # Analyze code
    analysis = client.analyze_code(sample_code, "javascript")
    print("Code Analysis:", analysis)
    
    # Generate documentation
    docs = client.generate_documentation(sample_code, "javascript")
    print("Documentation:", docs)
