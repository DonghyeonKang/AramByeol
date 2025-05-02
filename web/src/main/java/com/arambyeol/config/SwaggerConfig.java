package com.arambyeol.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI openAPI() {
        SecurityScheme securityScheme = new SecurityScheme()
                .type(SecurityScheme.Type.HTTP)
                .scheme("bearer")
                .bearerFormat("JWT")
                .in(SecurityScheme.In.HEADER)
                .name("Authorization");

        SecurityRequirement securityRequirement = new SecurityRequirement().addList("bearerAuth");

        Info info = new Info()
                .title("Arambyeol API Documentation")
                .version("v1.0")
                .description("아람별 프로젝트의 API 문서입니다.")
                .contact(new Contact()
                        .name("Arambyeol Team")
                        .email("your.email@example.com")
                        .url("https://github.com/yourusername/arambyeol"));

        return new OpenAPI()
                .components(new Components().addSecuritySchemes("bearerAuth", securityScheme))
                .addSecurityItem(securityRequirement)
                .info(info)
                .servers(List.of(
                    new Server().url("http://localhost:8080").description("Local Server"),
                    new Server().url("http://your-production-url").description("Production Server")
                ));
    }
} 