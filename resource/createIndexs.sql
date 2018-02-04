CREATE INDEX [call] ON [methodInvocationInfo]([callMethodName]) ;
CREATE INDEX [called] ON [methodInvocationInfo]([calledMethodName]) ;
CREATE INDEX [variable] ON [variableinfo](   [belongedMethod],  [isField]);
CREATE INDEX [distance] ON [simDistance](   [callMethodName],   [calledMethodName]);
