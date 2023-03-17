import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';

@Schema()
export class Job {
  @Prop()
  id: number;

  @Prop()
  name: string;

  @Prop()
  description: string;

  @Prop([String])
  skills: string[];

  @Prop([String])
  fields: string[];
}

export const JobSchema = SchemaFactory.createForClass(Job);
