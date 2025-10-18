from src.states.blogstate import BlogState
from langchain_core.messages import HumanMessage,SystemMessage
from src.states.blogstate import Blog


class BlogNode:
    """
    A Class to represent the blog node
    """

    def __init__(self,llm):
        self.llm = llm
    
    def title_creation(self,state:BlogState):
        """
        Create the title for the blog
        """

        if "topic" in state and state['topic']:
            prompt = """ 
                    You are an expert blog content writer. Use markdown formatting. Generate a blog title for the {topic}.
                    This should be creative and SEO friendly
                    """
            
            system_message = prompt.format(topic=state['topic'])
            response =self.llm.invoke(system_message)

            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        """
        Create teh content for the given topic
        """
        if "topic" in state and state['topic']:
            system_prompt = """
                    You are a expert blog writer. Use Markdown formatting.
                    Generate a detailed blog content with detailed breakdown for the {topic}
                    """
            system_message = system_prompt.format(topic=state['topic'])
            response = self.llm.invoke(system_message)
            
            return {"blog": {"title":state['blog']['title'], "content":response.content}}
        
    # def translation(self, state:BlogState):
    #     """
    #     Translate the content into specified language.
    #     """
    #     translation_prompt = """ 
    #                         Translate the following content into {current_language}.
    #                         - Maintain the original tone, style, and formatting.
    #                         - Adapt cultural references and idoms to be appropiate for {current_language}
    #
    #                         ORIGINAL CONTENT
    #                         {blog_content}
    #                         """
    #     blog_content = state['blog']['content']
    #     messages =[
    #         HumanMessage(translation_prompt.format(current_language=state['current_language'], blog_content=blog_content))
    #     ]
    #
    #     translation_content = self.llm.with_structured_output(Blog).invoke(messages)
    #     return {"blog": {"content": translation_content}}

    def translation(self, state:BlogState):
        """
        Translate the content into specified language.
        Always provide a title to Blog model.
        """
        translation_prompt = """
            Translate the following content into {current_language}.
            - Maintain the original tone, style, and formatting.
            - Adapt cultural references and idioms to be appropriate for {current_language}

            ORIGINAL CONTENT
            {blog_content}
        """
        blog_content = state['blog']['content']
        messages = [
            HumanMessage(translation_prompt.format(
                current_language=state['current_language'],
                blog_content=blog_content
            ))
        ]
        raw = self.llm.invoke(messages)
        # Extract only title/content fields
        original_title = state['blog'].get('title', '')
        if isinstance(raw, dict):
            filtered = {k: raw[k] for k in ['title', 'content'] if k in raw}
        else:
            filtered = {"content": str(raw)}
        # Always provide a title
        if 'title' not in filtered or not filtered['title']:
            filtered['title'] = original_title
        blog_obj = Blog(**filtered)
        return {"blog": {"title": blog_obj.title, "content": blog_obj.content}}
    
    
    def route(self, state:BlogState):
        return {"current_language":state['current_language']}
    

    def route_decision(self, state:BlogState):
        """
        Route the content to the respective translation function.
        Only allow mapped languages, fallback to 'french'.
        """
        lang = state.get("current_language", "french")
        if lang == "hindi":
            return "hindi"
        if lang == "french":
            return "french"
        # fallback branch so the graph doesn't error for other languages
        return "french"